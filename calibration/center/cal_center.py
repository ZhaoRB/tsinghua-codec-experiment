import math
import os

import cv2
import numpy as np
from parse_xml import data_structure, parse


# calculate all center points from three points
def calculateAllCentersOld(calibInfo: data_structure.CalibInfo) -> np.ndarray:
    allCenterPoints = np.zeros((calibInfo.rowNum, calibInfo.colNum, 2))

    xBias = calibInfo.diameter / 2 * math.sqrt(3)
    yBias = calibInfo.diameter / 2

    ltopOdd = np.array([calibInfo.ltop[0] + xBias, calibInfo.ltop[1] + yBias])

    colGap = (calibInfo.rtop - ltopOdd) / (calibInfo.colNum / 2 - 1)
    rowGap = (calibInfo.lbot - calibInfo.ltop) / (calibInfo.rowNum - 1)

    allCenterPoints[0, 0, :] = calibInfo.ltop
    allCenterPoints[0, 1, :] = ltopOdd

    for i in range(int(calibInfo.colNum - 2)):
        allCenterPoints[0, i + 2, :] = allCenterPoints[0, i, :] + colGap

    for r in range(int(calibInfo.rowNum - 1)):
        for c in range(int(calibInfo.colNum)):
            allCenterPoints[r + 1, c, :] = allCenterPoints[r, c, :] + rowGap

    return allCenterPoints


def calculateAllCenters(calibInfo: data_structure.CalibInfo) -> np.ndarray:
    allCenterPoints = np.zeros((calibInfo.rowNum, calibInfo.colNum, 2))

    xBias = calibInfo.diameter / 2 * math.sqrt(3)
    yBias = calibInfo.diameter / 2

    ltopOdd = np.array([calibInfo.ltop[0] + xBias, calibInfo.ltop[1] + yBias])

    colGap = (calibInfo.rtop - ltopOdd) / (calibInfo.colNum / 2 - 1)
    rowGap = (calibInfo.lbot - calibInfo.ltop) / (calibInfo.rowNum - 1)

    allCenterPoints[0, 0, :] = calibInfo.ltop
    allCenterPoints[0, 1, :] = ltopOdd

    for i in range(int(calibInfo.colNum - 2)):
        allCenterPoints[0, i + 2, :] = allCenterPoints[0, i, :] + colGap

    for r in range(int(calibInfo.rowNum - 1)):
        for c in range(int(calibInfo.colNum)):
            allCenterPoints[r + 1, c, :] = allCenterPoints[r, c, :] + rowGap

    return allCenterPoints


if __name__ == "__main__":
    projectPath = (
        "/home/zrb/project/tsinghua-codec-experiment"
    )

    calibrationFilePath = os.path.join(projectPath, "./cfg/test/tlct.xml")
    imageFilePath = os.path.join(projectPath, "./data/mini-garden/Image001.bmp")

    image = cv2.imread(imageFilePath)

    calibInfo = parse.parseCalibXmlFile(calibrationFilePath)
    allCenterPoints = calculateAllCenters(calibInfo)
