import os

import cv2
import numpy as np
from center.cal_center import calculateAllCenters
from parse_xml.parse import parseCalibXmlFile
from rotateAndCrop.crop import calCropPos, crop

# 1. set paths
projectPath = "/home/zrb/project/tsinghua-codec-experiment"
dataBaseFolder = "/data/MPEG148_TSPC_Sequences"
dataFolderName = "NewMiniGarden_0913_5000_far_020mm"

calibrationFilePath = os.path.join(projectPath, "./cfg/test/minigarden.xml")
input_folder = f"{dataBaseFolder}/{dataFolderName}"

output_folder = f"{dataBaseFolder}/cropped_{dataFolderName}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 2. parse calibration file and calulate center points
calibInfo = parseCalibXmlFile(calibrationFilePath)
print(calibInfo)

ltopX, ltopY, rbotX, rbotY = calCropPos(
    calibInfo.ltop, calibInfo.lbot, calibInfo.rtop, calibInfo.rbot, calibInfo.diameter
)

for i in range(301):  # 遍历 image000.bmp 到 image300.bmp
    image_name = f"Image{i:03d}.bmp"
    input_path = os.path.join(input_folder, image_name)

    if os.path.exists(input_path):
        raw_image = cv2.imread(input_path)

        # - process and save
        output_name = f"Image{i:03d}.bmp"
        output_path = os.path.join(output_folder, output_name)

        processed_image = crop(raw_image, ltopX, ltopY, rbotX, rbotY)
        cv2.imwrite(output_path, processed_image)

        print(f"Saved: {output_path}")
    else:
        print(f"File not found: {input_path}")
