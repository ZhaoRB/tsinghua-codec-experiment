import os

import cv2
from center.cal_center import calculateAllCenters
from center.draw_center import drawCenters
from parse_xml.parse import parseCalibXmlFile

# - set path
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
calibBasePath = "/home/zrb/data/mpeg148-tspc-seqs/calibration"
seqBasePath = "/home/zrb/data/mpeg148-tspc-seqs"

calibName = "Boys-fix.xml"
seqName = "Boys"

calibrationFilePath = os.path.join(projectPath, "./cfg/calibration", calibName)
inputPath = os.path.join(seqBasePath, seqName, "Image000.png")

image = cv2.imread(inputPath)

# output path
allCenterPath = os.path.join(projectPath, f"./data/center/allCenters_{seqName}.png")

# - parse calibration file and calulate center points
calibInfo = parseCalibXmlFile(calibrationFilePath)
print(calibInfo)

allCenterPoints = calculateAllCenters(calibInfo)

# - draw
# drawCenters(
#     image.copy(),
#     np.array([calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot]),
#     calibInfo.diameter,
#     cornerCenterPath,
# )

drawCenters(
    image.copy(),
    allCenterPoints.reshape(allCenterPoints.shape[0] * allCenterPoints.shape[1], 2),
    calibInfo.diameter,
    allCenterPath,
)
