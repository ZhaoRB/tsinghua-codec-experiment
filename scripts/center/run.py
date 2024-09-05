# %%
import os

import cv2
from cal_center import calculateAllCenters, parseCalibXmlFile
from draw_center import drawAllCenters, drawCornerCenters

projectPath = "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment"

calibrationFilePath = os.path.join(projectPath, "./cfg/test/tlct.xml")
imageFilePath = os.path.join(projectPath, "./data/mini-garden/Image001.bmp")

image = cv2.imread(imageFilePath)

calibInfo = parseCalibXmlFile(calibrationFilePath)
allCenterPoints = calculateAllCenters(calibInfo)

print(calibInfo)


# %%
# draw center
outputPath = os.path.join(projectPath, "./data/test-center/corner-centers.png")
cornerCentersImg = drawCornerCenters(
    image,
    calibInfo.ltop,
    calibInfo.rtop,
    calibInfo.lbot,
    calibInfo.rbot,
    calibInfo.diameter,
    outputPath,
)

outputPath = os.path.join(projectPath, "./data/test-center/all-centers.png")
allCentersImg = drawAllCenters(image, allCenterPoints, calibInfo.diameter, outputPath)

# %%
