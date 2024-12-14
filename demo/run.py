import csv
import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np
from utils import *

LL = 0
MV = 1


def getImagePattern(seq, qp: str, type, index=None):
    qpStr = f"qp{qp}" if qp.isdigit() else "base"
    folderName = "lenslet" if type == LL else "render"
    pattern = "Image%03d.png" if type == LL else "Frame%03d"

    os.makedirs(f"./data/output/{folderName}/{seq}_{qpStr}", exist_ok=True)
    path = f"./data/output/{folderName}/{seq}_{qpStr}/{pattern}"

    if type == MV and index is not None:
        path = (
            f"./data/output/{folderName}/{seq}_{qpStr}/{pattern}/image_{index:03}.png"
        )

    return path


def getYuvPath(seq, width, height, qp: str, type, index=None):
    qpStr = f"qp{qp}" if qp.isdigit() else "base"
    folderName = "lenslet" if type == LL else "render"
    os.makedirs(f"./data/output/{folderName}", exist_ok=True)

    path = f"./data/output/{folderName}/{seq}_{qpStr}_{width}x{height}_300frames_8bit_yuv420.yuv"
    if type == MV and index is not None:
        path = f"./data/output/{folderName}/{seq}_{qpStr}/{seq}_{qpStr}_{width}x{height}_300frames_8bit_yuv420_{index}.yuv"

    return path


def getCodecLogPath(seq, qp: str):
    os.makedirs("./data/output/log", exist_ok=True)
    return f"./data/output/log/{seq}_qp{qp}.log"


def getCsvFilePath(seq):
    os.makedirs("./data/output/summary", exist_ok=True)
    return f"./data/output/summary/{seq}.csv"


def getRDCurvePath(seq):
    os.makedirs("./data/output/summary", exist_ok=True)
    return f"./data/output/summary/{seq}.png"


def yuv2img(ffmpeg, width, height, inputYuv, outputImage):
    subprocess.run(
        [
            ffmpeg,
            "-s",
            f"{width}x{height}",
            "-pix_fmt",
            "yuv420p",
            "-i",
            inputYuv,
            "-start_number",
            "0",
            outputImage,
            "-y",
        ]
    )


def img2yuv(ffmpeg, inputImage, outputYuv):
    subprocess.run(
        [
            ffmpeg,
            "-start_number",
            "0",
            "-i",
            inputImage,
            "-vf",
            "format=yuv420p",
            "-frames:v",
            "300",
            outputYuv,
            "-y",
        ]
    )


def render(rlc, seq, qp: str):
    configFile = f"./config/{seq}/param.cfg"
    configData = {}

    with open(configFile, "r") as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                key, value = line.split(maxsplit=1)
                configData[key] = value.strip()

    configData["RawImage_Path"] = getImagePattern(seq, qp, LL)
    configData["Output_Path"] = getImagePattern(seq, qp, MV)

    with open(configFile, "w") as file:
        for key, value in configData.items():
            file.write(f"{key}\t{value}\n")

    subprocess.run([rlc, f"./config/{seq}/param.cfg"])


def decode(decoder, seq, width, height, qp: str):
    with open(getCodecLogPath(seq, qp), "w") as logfile:
        subprocess.run(
            [
                decoder,
                "-b",
                f"./data/input/bitstream/{seq}_qp{qp}.bin",
                "-o",
                getYuvPath(seq, width, height, qp, LL),
                "--OutputBitDepth=8",
                "--OutputBitDepthC=8",
            ],
            stdout=logfile,
        )


def summary(ffmpeg, seq, w, h, qps):
    seqCsvFilePath = getCsvFilePath(seq)
    headers = [
        "Sequence Name",
        "QP",
        "Bitrate(kbps)",
        "LLPSNR_Y(dB)",
        "LLPSNR_U(dB)",
        "LLPSNR_V(dB)",
        "MVPSNR_Y(dB)",
        "MVPSNR_U(dB)",
        "MVPSNR_V(dB)",
    ]

    with open(seqCsvFilePath, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for i in range(25):
            index = i + 1
            img2yuv(
                ffmpeg,
                getImagePattern(seq, "base", MV, index),
                getYuvPath(seq, w, h, "base", MV, index),
            )

        for qp in qps:
            logfile = f"./data/input/encoder-log/{seq}_qp{qp}.log"
            bitrate, llpsnr_y, llpsnr_u, llpsnr_v = extract_codec_info(logfile)

            mvpsnr_y, mvpsnr_u, mvpsnr_v = [], [], []

            for i in range(25):
                index = i + 1
                img2yuv(
                    ffmpeg,
                    getImagePattern(seq, qp, MV, index),
                    getYuvPath(seq, w, h, qp, MV, index),
                )

                baseYuv = getYuvPath(seq, w, h, "base", MV, index)
                curQpYuv = getYuvPath(seq, w, h, qp, MV, index)
                cur_mvpsnr_y, cur_mvpsnr_u, cur_mvpsnr_v = compute_psnr_for_yuv(
                    ffmpeg,
                    baseYuv,
                    curQpYuv,
                    w,
                    h,
                )

                mvpsnr_y.append(cur_mvpsnr_y)
                mvpsnr_u.append(cur_mvpsnr_u)
                mvpsnr_v.append(cur_mvpsnr_v)

            avg_mvpsnr_y, avg_mvpsnr_u, avg_mvpsnr_v = (
                sum(mvpsnr_y) / len(mvpsnr_y),
                sum(mvpsnr_u) / len(mvpsnr_u),
                sum(mvpsnr_v) / len(mvpsnr_v),
            )

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


def visualize(seq):
    with open(getCsvFilePath(seq), "r") as f:
        csv_data = csv.reader(f)
        next(csv_data)

        x_data = []
        y_data = []

        for row in csv_data:
            x_data.append(float(row[2]))  # Bitrate
            y_data.append(float(row[6]))  # MVPSNR_Y

        plt.plot(x_data, y_data, marker="o", linestyle="-", color="b")

        x_label = "Bitrate(kbps)"
        y_label = "MVPSNR_Y(dB)"

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(seq)
        plt.grid(True)

        x_min = 0
        x_max = max(x_data)
        x_margin = 0.1 * (x_max - x_min)
        x_max_adjusted = x_max + x_margin
        plt.xlim(x_min, x_max_adjusted)

        y_min, y_max = min(y_data), max(y_data)
        y_margin = 0.05 * (y_max - y_min)
        y_min_adjusted = y_min - y_margin
        y_max_adjusted = y_max + y_margin
        plt.ylim(y_min_adjusted, y_max_adjusted)
        tick_interval = 2
        yticks = np.arange(
            np.floor(y_min_adjusted),
            np.ceil(y_max_adjusted) + tick_interval,
            tick_interval,
        )
        plt.yticks(yticks)

        plt.savefig(getRDCurvePath(seq))
        plt.clf()


if __name__ == "__main__":
    ffmpeg = "./executable/ffmpeg"
    rlc40 = "./executable/RLC40"
    decoder = "./executable/DecoderAppStatic"

    seqName = "Boys2"
    qps = ["28", "32", "36", "40", "44", "48"]
    # qps = ["48"]
    llRes = [3976, 2956]
    mvRes = [1098, 800]

    # base
    yuv2img(
        ffmpeg,
        llRes[0],
        llRes[1],
        f"./data/input/raw-yuv/Boys2_3976x2956_300frames_8bit_yuv420.yuv",
        getImagePattern(seqName, "base", LL),
    )
    render(rlc40, seqName, "base")

    # codec
    for qp in qps:
        decode(decoder, seqName, llRes[0], llRes[1], qp)
        yuv2img(
            ffmpeg,
            llRes[0],
            llRes[1],
            getYuvPath(seqName, llRes[0], llRes[1], qp, LL),
            getImagePattern(seqName, qp, LL),
        )
        render(rlc40, seqName, qp)

    # summary
    summary(ffmpeg, seqName, mvRes[0], mvRes[1], qps)
    visualize(seqName)
