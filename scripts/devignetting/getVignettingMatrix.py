import math
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

projectPath = "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment"
whiteImagePath = os.path.join(projectPath, "./data/devignetting/whiteImage/0.2m.bmp")
centerMapPath = os.path.join(projectPath, "./data/center/centerPoints.npy")

radius = 35


def getVignettingMatrix() -> np.ndarray:
    whiteImage = cv2.imread(whiteImagePath)
    grayImage = cv2.cvtColor(whiteImage, cv2.COLOR_BGR2GRAY)
    grayImage = grayImage.astype(np.int_)

    centers: np.ndarray = np.load(centerMapPath)

    # drawCenter(whiteImage, centers)

    print(f"image size: {grayImage.shape}\ncenters size: {centers.shape}")

    vignettingMatrix = np.ones(grayImage.shape, dtype=np.float64)

    for row in centers:
        for point in row:
            for i in range(radius):
                centerX = round(point[0])
                centerY = round(point[1])
                centerLuma = grayImage[centerY, centerX]

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


def drawHeatMap(matrix):
    plt.imshow(matrix, cmap="hot", interpolation="none")
    plt.colorbar()
    plt.title("Heatmap without Interpolation")
    plt.show()


def drawCenter(image, allCenterPoints):
    image_copy = image.copy()

    for row in allCenterPoints:
        for point in row:
            center = (round(point[0]), round(point[1]))
            color = (0, 0, 255)
            cv2.circle(image_copy, center, radius, color, 2)

    cv2.imshow("centers", image_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    del image_copy


if __name__ == "__main__":
    matrix = getVignettingMatrix()
    savePath = os.path.join(projectPath, "./data/devignetting/coe/0.2m.npy")
    np.save(savePath, matrix)

    drawHeatMap(matrix)
