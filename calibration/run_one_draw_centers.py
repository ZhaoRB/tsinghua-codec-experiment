import cv2
import numpy as np
from center.cal_center import calculateAllCenters
from center.draw_center import drawCenters
from parse_xml.parse import parseCalibXmlFile

# - set path
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
seqPath = "/home/data/1003Sequences/zrb"
name = "NewMiniGarden"
seqName = f"cropped-restore-{name}-5000"

calibrationFilePath = f"{projectPath}/cfg/1003/cropped_{name}.xml"
inputPath = f"{seqPath}/{seqName}/Image001.png"

image = cv2.imread(inputPath)

# output path
cornerCenterPath = f"{projectPath}/data/center/four_center_{seqName}.png"
allCenterPath = f"{projectPath}/data/center/all_center_{seqName}.png"

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
