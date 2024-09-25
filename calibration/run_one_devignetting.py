import os

import cv2
import numpy as np
from center.cal_center import calculateAllCenters
from center.draw_center import drawCenters
from devignetting.devignetting import (
    devignetting,
    drawHeatMap,
    getVignettingMatrix,
    getVignettingMatrixNew,
)
from parse_xml.parse import parseCalibXmlFile
from rotateAndCrop.rotate import rotate

# - set path
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
nameMap = {
    "boys": "Boys_fix_color",
    "minigarden": "MiniGarden",
    "motherboard": "Motherboard",
}
name = "boys"

calibrationFilePath = os.path.join(projectPath, f"./cfg/test/{name}.xml")
inputPath = os.path.join(projectPath, f"./data/sample/{nameMap[name]}.png")
image = cv2.imread(inputPath)

# output path
cornerCenterPath = os.path.join(
    projectPath, f"./data/corner-center/{nameMap[name]}.png"
)
allCenterPath = os.path.join(projectPath, f"./data/all-center/{nameMap[name]}.png")
devignettingPath = os.path.join(projectPath, f"./data/devignetting/{nameMap[name]}.png")
rotatePath = os.path.join(projectPath, f"./data/rotate/{nameMap[name]}.png")
fixColorPath = os.path.join(projectPath, f"./data/fix-color/{nameMap[name]}.png")


# - parse calibration file and calulate center points
calibInfo = parseCalibXmlFile(calibrationFilePath)
print(calibInfo)

allCenterPoints = calculateAllCenters(calibInfo)

# - draw
drawCenters(
    image.copy(),
    np.array([calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot]),
    calibInfo.diameter,
    cornerCenterPath,
)

drawCenters(
    image.copy(),
    allCenterPoints.reshape(allCenterPoints.shape[0] * allCenterPoints.shape[1], 2),
    calibInfo.diameter,
    allCenterPath,
)

# - draw white image centers
whiteImageName = "0.2m"
whiteImage = cv2.imread(
    os.path.join(projectPath, f"./data/whiteImage/{whiteImageName}.bmp")
)
whiteCornerCenterPath = os.path.join(
    projectPath, f"./data/corner-center/{whiteImageName}_{name}.png"
)
whiteAllCenterPath = os.path.join(
    projectPath, f"./data/all-center/{whiteImageName}_{name}.png"
)

drawCenters(
    whiteImage.copy(),
    np.array([calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot]),
    calibInfo.diameter,
    whiteCornerCenterPath,
)

drawCenters(
    whiteImage.copy(),
    allCenterPoints.reshape(allCenterPoints.shape[0] * allCenterPoints.shape[1], 2),
    calibInfo.diameter,
    whiteAllCenterPath,
)

# - devignetting
heatMapPath = os.path.join(
    projectPath, f"./data/devignetting/heat_{whiteImageName}_{name}.png"
)

vignettingMatrix = getVignettingMatrixNew(
    whiteImage, allCenterPoints, calibInfo.diameter // 2
)
drawHeatMap(vignettingMatrix, heatMapPath, True)

devignetting(image, vignettingMatrix, devignettingPath)
