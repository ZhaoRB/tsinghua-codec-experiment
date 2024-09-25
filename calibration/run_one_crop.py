import math
import os

import cv2
import numpy as np
from center.cal_center import calculateAllCenters
from center.draw_center import drawCenters
from parse_xml.parse import parseCalibXmlFile

# - set path
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
nameMap = {
    "boys": "Boys_fix_color",
    "minigarden": "newMiniGarden",
    "motherboard": "Motherboard",
}
name = "minigarden"

calibrationFilePath = os.path.join(projectPath, f"./cfg/test/{name}.xml")
inputPath = os.path.join(projectPath, f"./data/sample/{nameMap[name]}.bmp")
image = cv2.imread(inputPath)

# output path
cornerCenterPath = os.path.join(
    projectPath, f"./data/corner-center/{nameMap[name]}.png"
)
allCenterPath = os.path.join(projectPath, f"./data/all-center/{nameMap[name]}.png")
cropPath = os.path.join(projectPath, f"./data/crop/{nameMap[name]}.png")


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

# - crop


