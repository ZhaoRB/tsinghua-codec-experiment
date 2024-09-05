import xml.etree.ElementTree as ET

import cv2
import numpy as np


def drawCornerCenters(
    image: np.ndarray,
    ltop: np.ndarray,
    rtop: np.ndarray,
    lbot: np.ndarray,
    rbot: np.ndarray,
    diameter,
    outputPath,
):
    image_copy = image.copy()

    for point in [ltop, rtop, lbot, rbot]:
        if point.shape[0] == 0:
            continue
        center = (round(point[0]), round(point[1]))
        color = (0, 0, 255)
        Thickness = 1
        cv2.circle(image_copy, center, diameter // 2, color, Thickness)

    cv2.imwrite(outputPath, image_copy)


def drawAllCenters(image: np.ndarray, allCenterPoints: np.ndarray, diameter, outputPath):
    image_copy = image.copy()

    for row in allCenterPoints:
        for point in row:
            center = (round(point[0]), round(point[1]))
            color = (0, 0, 255)
            Thickness = 1
            cv2.circle(image_copy, center, diameter // 2, color, Thickness)

    cv2.imwrite(outputPath, image_copy)


if __name__ == "__main__":
    calibrationFilePath = "/Users/riverzhao/Project/Codec/0_lvc_codec/Inter-MCA/config/new-seq/tlct.xml"
    imageFilePath = "/Users/riverzhao/Project/Codec/0_lvc_codec/Inter-MCA/data/raw/miniGarden.bmp"

    image = cv2.imread(imageFilePath)
    output_path = "/Users/riverzhao/Project/Codec/0_lvc_codec/Inter-MCA/data/center/new-seq/three-points.png"
