import math
import os
import xml.etree.ElementTree as ET

import cv2
import numpy as np
from data_structure import CalibInfo


def parseCalibXmlFile(calibrationFilePath) -> CalibInfo:
    tree = ET.parse(calibrationFilePath)
    root = tree.getroot()

    diameterNode = root.find("diameter")
    diameter = int(diameterNode.text)
    centersNode = root.find("centers")
    rowNode = centersNode.find("rows")
    rowNum = int(rowNode.text)
    colNode = centersNode.find("cols")
    colNum = int(colNode.text)

    ltop = np.array(
        [
            float(centersNode.find("ltop").find("x").text),
            float(centersNode.find("ltop").find("y").text),
        ]
    )
    rtop = np.array(
        [
            float(centersNode.find("rtop").find("x").text),
            float(centersNode.find("rtop").find("y").text),
        ]
    )
    lbot = np.array(
        [
            float(centersNode.find("lbot").find("x").text),
            float(centersNode.find("lbot").find("y").text),
        ]
    )

    if centersNode.find("rbot") is not None:
        rbot = np.array(
            [
                float(centersNode.find("rbot").find("x").text),
                float(centersNode.find("rbot").find("y").text),
            ]
        )
    else:
        rbot = np.array([])

    return CalibInfo(diameter, rowNum, colNum, ltop, rtop, lbot, rbot)


# calculate all center points from three points
def calculateAllCenters(calibInfo: CalibInfo) -> np.ndarray:
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
        "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment"
    )

    calibrationFilePath = os.path.join(projectPath, "./cfg/test/tlct.xml")
    imageFilePath = os.path.join(projectPath, "./data/mini-garden/Image001.bmp")

    image = cv2.imread(imageFilePath)

    calibInfo = parseCalibXmlFile(calibrationFilePath)
    allCenterPoints = calculateAllCenters(calibInfo)

    # print(image.shape, image.shape[1])

    # np.save("centerPoints.npy", allCenterPoints)
