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
from rotate.rotate import rotate

# 1. set paths
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
dataBaseFolder = "/data/ZRB/0913-seq"
dataFolderName = "0913_5000_02mm"


calibrationFilePath = os.path.join(projectPath, f"./cfg/test/minigarden.xml")
input_folder = f"{dataBaseFolder}/{dataFolderName}"

# output folder path
devignettingFolder = os.path.join(
    projectPath, f"{dataBaseFolder}/devignetting_{dataFolderName}"
)
rotateFolder = os.path.join(projectPath, f"{dataBaseFolder}/rotate_{dataFolderName}")
fixColorFolder = os.path.join(
    projectPath, f"{dataBaseFolder}/fix_color_{dataFolderName}"
)

output_folder = devignettingFolder


# 2. parse calibration file and calulate center points
calibInfo = parseCalibXmlFile(calibrationFilePath)
print(calibInfo)

allCenterPoints = calculateAllCenters(calibInfo)

# 3. process: rotate, devignetting or fix color
# whiteImageName = "0.2m"
# whiteImage = cv2.imread(
#     os.path.join(projectPath, f"./data/whiteImage/{whiteImageName}.bmp")
# )
# vignettingMatrix = getVignettingMatrixNew(
#     whiteImage, allCenterPoints, calibInfo.diameter // 2
# )

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for i in range(301):  # 遍历 image000.bmp 到 image300.bmp
    image_name = f"Image{i:03d}.bmp"
    input_path = os.path.join(input_folder, image_name)

    if os.path.exists(input_path):
        raw_image = cv2.imread(input_path)

        # - process and save
        output_name = f"Image{i:03d}.png"
        output_path = os.path.join(output_folder, output_name)
        # devignetting(raw_image, vignettingMatrix, output_path)
        rotatedImage = rotate(raw_image, calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot)
        cv2.imwrite(output_path, rotatedImage)

        print(f"Saved: {output_path}")
    else:
        print(f"File not found: {input_path}")
