import os

import cv2
import numpy as np
from center.cal_center import calculateAllCenters
from parse_xml.parse import parseCalibXmlFile
from rotateAndCrop.rotate import rotate

# 1. set paths
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
dataBaseFolder = "/data/ZRB/0913-seq"
dataFolderName = "0913_5000_02mm"
calibFileName = "minigarden"


calibrationFilePath = os.path.join(projectPath, f"./cfg/test/{calibFileName}.xml")
input_folder = f"{dataBaseFolder}/{dataFolderName}"

rotateFolder = os.path.join(projectPath, f"{dataBaseFolder}/rotate_{dataFolderName}")

# 2. parse calibration file and calulate center points
calibInfo = parseCalibXmlFile(calibrationFilePath)
print(calibInfo)

allCenterPoints = calculateAllCenters(calibInfo)


if not os.path.exists(rotateFolder):
    os.makedirs(rotateFolder)

for i in range(301):  # 遍历 image000.bmp 到 image300.bmp
    image_name = f"Image{i:03d}.bmp"
    input_path = os.path.join(input_folder, image_name)

    if os.path.exists(input_path):
        raw_image = cv2.imread(input_path)

        # - process and save
        output_name = f"Image{i:03d}.bmp"
        output_path = os.path.join(rotateFolder, output_name)
        
        rotatedImage = rotate(raw_image, calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot)
        cv2.imwrite(output_path, rotatedImage)

        print(f"Saved: {output_path}")
    else:
        print(f"File not found: {input_path}")
