"""
- 原理:
    假设认为，MI中心的像素是最亮的，周围的像素相对于MI中心点，亮度存在衰减，需要后期补偿回来

- 方法:
    拍摄白图像（白纸），使用白图像计算这个衰减的矩阵，并用这个矩阵去补偿序列图像
"""

import math
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np


def getVignettingMatrix(
    whiteImage: np.ndarray, centers: np.ndarray, radius
) -> np.ndarray:
    grayImage = cv2.cvtColor(whiteImage, cv2.COLOR_BGR2GRAY)
    grayImage = grayImage.astype(np.int_)

    vignettingMatrix = np.ones(grayImage.shape, dtype=np.float64)

    for row in centers:
        for point in row:
            centerX = round(point[0])
            centerY = round(point[1])
            centerLuma = grayImage[centerY, centerX]

            for i in range(radius):
                avgLuma = (
                    grayImage[centerY + i, centerX]
                    + grayImage[centerY - i, centerX]
                    + grayImage[centerY, centerX + i]
                    + grayImage[centerY, centerX - i]
                ) / 4
                ratio = avgLuma / centerLuma
                if ratio > 1:
                    ratio = 1

                vignettingMatrix[centerY + i, centerX] = ratio
                vignettingMatrix[centerY - i, centerX] = ratio
                vignettingMatrix[centerY, centerX + i] = ratio
                vignettingMatrix[centerY, centerX - i] = ratio

                for j in range(i + 1):
                    if math.sqrt(i**2 + j**2) < radius:
                        avgLuma = (
                            grayImage[centerY + i, centerX + j]
                            + grayImage[centerY + i, centerX - j]
                            + grayImage[centerY - i, centerX + j]
                            + grayImage[centerY - i, centerX - j]
                            + grayImage[centerY + j, centerX - i]
                            + grayImage[centerY + j, centerX + i]
                            + grayImage[centerY - j, centerX - i]
                            + grayImage[centerY - j, centerX + i]
                        ) / 8
                        ratio = avgLuma / centerLuma
                        if ratio > 1:
                            ratio = 1

                        vignettingMatrix[centerY + i, centerX + j] = ratio
                        vignettingMatrix[centerY + i, centerX - j] = ratio
                        vignettingMatrix[centerY - i, centerX + j] = ratio
                        vignettingMatrix[centerY - i, centerX - j] = ratio
                        vignettingMatrix[centerY + j, centerX - i] = ratio
                        vignettingMatrix[centerY + j, centerX + i] = ratio
                        vignettingMatrix[centerY - j, centerX - i] = ratio
                        vignettingMatrix[centerY - j, centerX + i] = ratio

    return vignettingMatrix


def getVignettingMatrixNew(whiteImage: np.ndarray, centers: np.ndarray, radius):
    grayImage = cv2.cvtColor(whiteImage, cv2.COLOR_BGR2GRAY)
    grayImage = grayImage.astype(np.int_)

    vignettingMatrix = np.ones(grayImage.shape, dtype=np.float64)

    for row in centers:
        for point in row:
            centerX = round(point[0])
            centerY = round(point[1])
            centerLuma = grayImage[centerY, centerX]

            for i in range(radius):
                vignettingMatrix[centerY + i, centerX] = grayImage[centerY + i, centerX] / centerLuma
                vignettingMatrix[centerY - i, centerX] = grayImage[centerY - i, centerX] / centerLuma
                vignettingMatrix[centerY, centerX + i] = grayImage[centerY, centerX + i] / centerLuma
                vignettingMatrix[centerY, centerX - i] = grayImage[centerY, centerX - i] / centerLuma

                for j in range(i + 1):
                    if math.sqrt(i**2 + j**2) < radius:
                        vignettingMatrix[centerY + i, centerX + j] = grayImage[centerY + i, centerX + j] / centerLuma
                        vignettingMatrix[centerY + i, centerX - j] = grayImage[centerY + i, centerX - j] / centerLuma
                        vignettingMatrix[centerY - i, centerX + j] = grayImage[centerY - i, centerX + j] / centerLuma
                        vignettingMatrix[centerY - i, centerX - j] = grayImage[centerY - i, centerX - j] / centerLuma
                        vignettingMatrix[centerY + j, centerX - i] = grayImage[centerY + j, centerX - i] / centerLuma
                        vignettingMatrix[centerY + j, centerX + i] = grayImage[centerY + j, centerX + i] / centerLuma
                        vignettingMatrix[centerY - j, centerX - i] = grayImage[centerY - j, centerX - i] / centerLuma
                        vignettingMatrix[centerY - j, centerX + i] = grayImage[centerY - j, centerX + i] / centerLuma
    for i in range(vignettingMatrix.shape[0]):
        for j in range(vignettingMatrix.shape[1]):
            if vignettingMatrix[i, j] > 1:
                vignettingMatrix[i, j] = 1

    return vignettingMatrix

def drawHeatMap(matrix, savePath, show: bool):
    plt.imshow(matrix, cmap="hot", interpolation="none")
    plt.colorbar()
    plt.title("Heatmap without Interpolation")
    if show:
        plt.show()
    plt.savefig(savePath)


def devignetting(raw_image: np.ndarray, vignettingMatrix: np.ndarray, savePath):
    vignettingMatrix_ = vignettingMatrix[:, :, np.newaxis]
    devignetedImage = raw_image / vignettingMatrix_

    cv2.imwrite(savePath, devignetedImage)
