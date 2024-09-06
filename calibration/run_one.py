import os

import cv2
import numpy as np
from center.cal_center import calculateAllCenters
from center.draw_center import drawCenters
from parse_xml.parse import parseCalibXmlFile
from rotate.rotate import rotate

# 1. set path
projectPath = "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment"
nameMap = {
    "boys": "Boys_fix_color",
    "minigarden": "MiniGarden",
    "motherboard": "Motherboard",
}
name = "minigarden"

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


# 2. parse calibration file and calulate center points
calibInfo = parseCalibXmlFile(calibrationFilePath)
print(calibInfo)

allCenterPoints = calculateAllCenters(calibInfo)

# 3. process


# 4. draw
drawCenters(
    image,
    np.array([calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot]),
    calibInfo.diameter,
    cornerCenterPath,
)

drawCenters(
    image,
    allCenterPoints.reshape(allCenterPoints.shape[0] * allCenterPoints.shape[1], 2),
    calibInfo.diameter,
    allCenterPath,
)
