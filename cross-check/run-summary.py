import csv
import os

from initialize import *
from utils.extract import extract_codec_info, if_codec_finish
from utils.psnr import compute_psnr_for_yuv

# Open the CSV file for writing
with open(csvFileName, mode="w", newline="") as csvfile:
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

    for seq in all_seqs:
        for qp in all_qps[seq]:
            logfile = os.path.join(codecOutputFolder, f"{seq}_qp{qp}.log")

            # check if log file exists and if codec finished
            if not os.path.exists(logfile) or not if_codec_finish(logfile):
                continue

            bitrate, llpsnr_y, llpsnr_u, llpsnr_v = extract_codec_info(logfile)

            baseYuv = getBaseRenderYuvPath(seq)
            curQpYuv = getRenderYuvPath(seq, qp)

            mvpsnr_y, mvpsnr_u, mvpsnr_v = [" ", " ", " "]
            if os.path.exists(baseYuv) and os.path.exists(curQpYuv):
                mvpsnr_y, mvpsnr_u, mvpsnr_v = compute_psnr_for_yuv(
                    baseYuv,
                    curQpYuv,
                    rendered_resolutions[seq][0],
                    rendered_resolutions[seq][1],
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
                    mvpsnr_y,
                    mvpsnr_u,
                    mvpsnr_v,
                ]
            )
