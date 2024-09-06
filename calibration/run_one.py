import os

import cv2
import numpy as np
from center.cal_center import calculateAllCenters
from center.draw_center import drawAllCenters, drawCornerCenters
from parse_xml.parse import parseCalibXmlFile
from rotate.rotate import rotate

# 1. set path
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
nameMap = {
    "boys": "Boys_fix_color",
    "minigarden": "MiniGarden",
    "motherboard": "Motherboard",
}
name = "minigarden"

calibrationFilePath = os.path.join(projectPath, f"./cfg/test/{name}.xml")
inputPath = os.path.join(projectPath, f"./data/sample/{nameMap[name]}.png")

# output path
cornerCenterPath = os.path.join(projectPath, f"./data/corner-center/{nameMap[name]}.png")
allCenterPath = os.path.join(projectPath, f"./data/all-center/{nameMap[name]}.png")
devignettingPath = os.path.join(projectPath, f"./data/devignetting/{nameMap[name]}.png")
rotatePath = os.path.join(projectPath, f"./data/rotate/{nameMap[name]}.png")
fixColorPath = os.path.join(projectPath, f"./data/fixColor/{nameMap[name]}.png")


# 2. parse calibration file and calulate center points
calibInfo = parseCalibXmlFile(calibrationFilePath)
print(calibInfo)

allCenterPoints = calculateAllCenters(calibInfo)


# 3. process