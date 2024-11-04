# import cv2
# import numpy as np
# from center.cal_center import calculateAllCenters
# from center.draw_center import drawCenters
# from parse_xml.parse import parseCalibXmlFile

# # - set path
# projectPath = "/home/zrb/project/tsinghua-codec-experiment"
# seqPath = "/home/zrb/project/tsinghua-codec-experiment/data/sample"
# name = "Matryoshka"
# seqName = name

# calibrationFilePath = f"{projectPath}/cfg/{name}.xml"
# inputPath = f"{seqPath}/{seqName}.bmp"

# image = cv2.imread(inputPath)

# # output path
# cornerCenterPath = f"{projectPath}/data/center/four_center_{seqName}.png"
# allCenterPath = f"{projectPath}/data/center/all_center_{seqName}.png"

# # - parse calibration file and calulate center points
# calibInfo = parseCalibXmlFile(calibrationFilePath)
# print(calibInfo)

# allCenterPoints = calculateAllCenters(calibInfo)

# # - draw
# drawCenters(
#     image.copy(),
#     np.array([calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot]),
#     calibInfo.diameter,
#     cornerCenterPath,
# )

# # drawCenters(
# #     image.copy(),
# #     allCenterPoints.reshape(allCenterPoints.shape[0] * allCenterPoints.shape[1], 2),
# #     calibInfo.diameter,
# #     allCenterPath,
# # )


import cv2
import numpy as np
from center.cal_center import calculateAllCenters
from center.draw_center import drawCenters
from parse_xml.parse import parseCalibXmlFile

# - set path
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
seqPath = "/home/zrb/project/tsinghua-codec-experiment/data/sample"
name = "Matryoshka"
seqName = name

calibrationFilePath = f"{projectPath}/cfg/{name}.xml"
inputPath = f"{seqPath}/{seqName}.bmp"

cornerCenterPath = f"{projectPath}/data/center/four_center_{seqName}.png"
allCenterPath = f"{projectPath}/data/center/all_center_{seqName}.png"

# Read the image
image = cv2.imread(inputPath)

# Set brightness threshold
brightness_threshold = 7  # Example threshold

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply the brightness threshold
_, bright_mask = cv2.threshold(gray_image, brightness_threshold, 255, cv2.THRESH_BINARY)

# Convert mask to a 3-channel image (to match the original image for visualization)
bright_image = cv2.merge([bright_mask, bright_mask, bright_mask])

# - parse calibration file and calculate center points
calibInfo = parseCalibXmlFile(calibrationFilePath)
print(calibInfo)

allCenterPoints = calculateAllCenters(calibInfo)

# # - draw centers on the processed image
# drawCenters(
#     bright_image.copy(),
#     np.array([calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot]),
#     calibInfo.diameter,
#     cornerCenterPath,
# )

# Uncomment and use `bright_image` instead if centers should be drawn on the thresholded image
drawCenters(
    image.copy(),
    allCenterPoints.reshape(allCenterPoints.shape[0] * allCenterPoints.shape[1], 2),
    calibInfo.diameter,
    allCenterPath,
)
