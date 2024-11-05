import csv
import os

import matplotlib.pyplot as plt
from initialize import *

# 定义常量，表示列索引
X_AXIS_QP = 0
X_AXIS_BITRATE = 1
Y_AXIS_LLPSNR = 0
Y_AXIS_MVPSNR = 1


def get_figure_name(seq, xType, yType):
    names = [
        f"{seq}-qp-llpsnr",
        f"{seq}-qp-mvpsnr",
        f"{seq}-bitrate-llpsnr",
        f"{seq}-bitrate-mvpsnr",
    ]

    return names[xType * 2 + yType]


def draw_rd_curve(csvFilePath, xType, yType, figurePath):
    with open(csvFilePath, "r") as f:
        csv_data = csv.reader(f)
        next(csv_data)

        x_data = []
        y_data = []

        for row in csv_data:
            # 根据xType选择横轴数据
            if xType == X_AXIS_QP:
                x_data.append(float(row[1]))  # QP列
            elif xType == X_AXIS_BITRATE:
                x_data.append(float(row[2]))  # Bitrate列

            # 根据yType选择纵轴数据
            if yType == Y_AXIS_LLPSNR:
                y_data.append(float(row[3]))  # LLPSNR_Y列
            elif yType == Y_AXIS_MVPSNR:
                y_data.append(float(row[6]))  # MVPSNR_Y列

            sequence_name = row[0]

        # 绘制曲线图
        plt.plot(x_data, y_data, marker="o", linestyle="-", color="b")

        # 设置图形标题和轴标签
        x_label = "QP" if xType == X_AXIS_QP else "Bitrate(kbps)"
        y_label = "LLPSNR_Y(dB)" if yType == Y_AXIS_LLPSNR else "MVPSNR_Y(dB)"

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(sequence_name)
        plt.grid(True)

        # 保存图像到指定路径
        figureName = get_figure_name(sequence_name, xType, yType)
        outputFilePath = os.path.join(figurePath, figureName + ".png")
        os.makedirs(figurePath, exist_ok=True)

        plt.savefig(outputFilePath)

        # 清除当前图像，避免影响后续绘图
        plt.clf()


if __name__ == "__main__":
    for seq in seqs:
        csvFilePath = os.path.join(summaryOutputFolder, f"{seq}_summary.csv")
        if not os.path.exists(csvFilePath):
            print(f"csv file does not exist: {csvFilePath}")
            continue
        draw_rd_curve(csvFilePath, X_AXIS_BITRATE, Y_AXIS_MVPSNR, summaryOutputFolder)
        # draw_rd_curve(csvFilePath, X_AXIS_BITRATE, Y_AXIS_MVPSNR, baseFolder)
