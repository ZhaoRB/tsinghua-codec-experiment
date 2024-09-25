import os

import cv2
import numpy as np
from center.cal_center import calculateAllCenters
from center.draw_center import drawCenters
from parse_xml.parse import parseCalibXmlFile
from rotateAndCrop.crop import calCropPos, crop
from rotateAndCrop.rotate import rotate

# - set path
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
name = "boys"
seq_name = "boys_fix_color"

calibrationFilePath = os.path.join(projectPath, f"./cfg/test/{name}.xml")
inputPath = os.path.join(projectPath, f"./data/sample/{seq_name}.bmp")
image = cv2.imread(inputPath)

# output path
fourCenterPath = os.path.join(projectPath, f"./data/center/four_{seq_name}.png")
rotatePath = os.path.join(projectPath, f"./data/cropAndRotate/rotate_{seq_name}.bmp")
cropAndRotatePath = os.path.join(
    projectPath, f"./data/cropAndRotate/cropAndRotate_{seq_name}.bmp"
)

# - parse calibration file and calulate center points
calibInfo = parseCalibXmlFile(calibrationFilePath)
print(calibInfo)

# - draw
drawCenters(
    image.copy(),
    np.array([calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot]),
    calibInfo.diameter,
    fourCenterPath,
)

# test in one image
# rotate
rotated_image, rotated_points = rotate(
    image, calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot
)
cv2.imwrite(rotatePath, rotated_image)

ltop, rtop, lbot, rbot = rotated_points
testImage = drawCenters(
    rotated_image.copy(),
    np.array([ltop, rtop, lbot, rbot]),
    calibInfo.diameter,
    fourCenterPath,
)

ltopX, ltopY, rbotX, rbotY = calCropPos(
    ltop, lbot, rtop, rbot, calibInfo.diameter, True
)
rotated_cropped_image = crop(rotated_image, ltopX, ltopY, rbotX, rbotY)
cv2.imwrite(cropAndRotatePath, rotated_cropped_image)

