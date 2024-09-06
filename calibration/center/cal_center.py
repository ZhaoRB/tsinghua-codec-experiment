import math
import os

import cv2
import numpy as np
from parse_xml import data_structure, parse


# calculate all center points from three points (calibration file old version)
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


# calculate all center points from four points
def calculateAllCenters(calibInfo: data_structure.CalibInfo) -> np.ndarray:
    ltop, rtop, lbot, rbot, colNum, rowNum = (
        calibInfo.ltop,
        calibInfo.rtop,
        calibInfo.lbot,
        calibInfo.rbot,
        calibInfo.colNum,
        calibInfo.rowNum,
    )

    allCenterPoints = np.zeros((rowNum, colNum, 2))

    # colNum - 2: one column on the right of rtop: -1, distance -1
    distance_col = (rtop - ltop) / (colNum - 2)

    for col in range(colNum):
        ratioL = (colNum - 1 - col) / (colNum - 1)
        ratioR = col / (colNum - 1)
        distance_row = (ratioL * (lbot - ltop) + ratioR * (rbot - rtop)) / (rowNum - 1)

        firstPoint = ltop + distance_col * col
        if col % 2 == 1:
            firstPoint = firstPoint + distance_row / 2
        allCenterPoints[0, col] = firstPoint
        
        for row in range(rowNum - 1):
            cur = row + 1
            allCenterPoints[cur, col] = allCenterPoints[cur - 1, col] + distance_row

    return allCenterPoints

        


if __name__ == "__main__":
    projectPath = "/home/zrb/project/tsinghua-codec-experiment"

    calibrationFilePath = os.path.join(projectPath, "./cfg/test/tlct.xml")
    imageFilePath = os.path.join(projectPath, "./data/mini-garden/Image001.bmp")

    image = cv2.imread(imageFilePath)

    calibInfo = parse.parseCalibXmlFile(calibrationFilePath)
    allCenterPoints = calculateAllCenters(calibInfo)
