import csv
import os

from initialize import *
from tasks.format_convert import img2yuv
from utils.extract import extract_codec_info, if_codec_finish
from utils.psnr import compute_psnr_for_yuv

summaryLogFile = os.path.join(summaryOutputFolder, "summary.log")


def run_summary(seq):
    seqCsvFileName = getSeqCsvFileName(seq)

    with open(seqCsvFileName, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Sequence Name",
                "QP",
                "Bitrate",
                "LLPSNR_Y",
                "LLPSNR_U",
                "LLPSNR_V",
                "MVPSNR_Y",
                "MVPSNR_U",
                "MVPSNR_V",
            ]
        )

        for i in range(viewNum * viewNum):
            index = i + 1
            curImagePattern = f"image_{index:03}.png"

            img2yuv(
                ffmpeg,
                startFrame,
                frames,
                os.path.join(getBaseRenderFramePattern(seq), curImagePattern),
                getSummaryTempBaseYuv(seq, index),
                summaryLogFile,
            )

        for qp in qps[seq]:
            # 1. get bitrate and llpsnr from vvc logfile
            logfile = os.path.join(codecOutputFolder, f"{seq}_qp{qp}.log")

            # check if log file exists and if codec finished
            if not os.path.exists(logfile) or not if_codec_finish(logfile):
                continue

            bitrate, llpsnr_y, llpsnr_u, llpsnr_v = extract_codec_info(logfile)

            # 2. calculate mvpsnr from all view points
            mvpsnr_y, mvpsnr_u, mvpsnr_v = [], [], []

            for i in range(viewNum * viewNum):
                index = i + 1
                curImagePattern = f"image_{index:03}.png"

                baseYuv = getSummaryTempBaseYuv(seq, index)
                curQpYuv = getSummaryTempQpYuv(seq, qp, index)

                img2yuv(
                    ffmpeg,
                    startFrame,
                    frames,
                    os.path.join(getRenderFramePattern(seq, qp), curImagePattern),
                    curQpYuv,
                    summaryLogFile,
                )

                cur_mvpsnr_y, cur_mvpsnr_u, cur_mvpsnr_v = compute_psnr_for_yuv(
                    baseYuv,
                    curQpYuv,
                    rendered_resolutions[seq][0],
                    rendered_resolutions[seq][1],
                )

                mvpsnr_y.append(cur_mvpsnr_y)
                mvpsnr_u.append(cur_mvpsnr_u)
                mvpsnr_v.append(cur_mvpsnr_v)

            avg_mvpsnr_y, avg_mvpsnr_u, avg_mvpsnr_v = (
                sum(mvpsnr_y) / len(mvpsnr_y),
                sum(mvpsnr_u) / len(mvpsnr_u),
                sum(mvpsnr_v) / len(mvpsnr_v),
            )

            # Write data row for the current sequence and qp value
            writer.writerow(
                [
                    seq,
                    qp,
                    bitrate,
                    llpsnr_y,
                    llpsnr_u,
                    llpsnr_v,
                    avg_mvpsnr_y,
                    avg_mvpsnr_u,
                    avg_mvpsnr_v,
                ]
            )


def mergeAllCsvFiles():
    with open(csvFileNameAllSeqs, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Sequence Name",
                "QP",
                "Bitrate",
                "LLPSNR_Y",
                "LLPSNR_U",
                "LLPSNR_V",
                "MVPSNR_Y",
                "MVPSNR_U",
                "MVPSNR_V",
            ]
        )

    for seq in seqs:
        if os.path.exists(getSeqCsvFileName(seq)):
            with open(getSeqCsvFileName(seq), mode="r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    writer.writerow(row)


if __name__ == "__main__":
    for seq in seqs:
        run_summary(seq)

    mergeAllCsvFiles()
