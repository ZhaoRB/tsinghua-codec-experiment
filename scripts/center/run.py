import os
import sys

import cv2
import numpy as np
from cal_center import calculateAllCenters, parseCalibXmlFile
from draw_center import drawAllCenters, drawCornerCenters

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rotate.rotate import rotate


if __name__ == "__main__":
    projectPath = (
        "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment"
    )

    calibrationFilePath = os.path.join(projectPath, "./cfg/test/tlct.xml")

    imageFilePath = os.path.join(projectPath, "./data/mini-garden/Image001.bmp")
    image = cv2.imread(imageFilePath)

    # - parse calibration file and calulate center points
    calibInfo = parseCalibXmlFile(calibrationFilePath)
    print(calibInfo)

    # - calculate center points
    allCenterPoints = calculateAllCenters(calibInfo)
    # np.save()

    # - draw center
    outputPath = os.path.join(projectPath, "./data/test-center/corner-centers.png")
    drawCornerCenters(
        image,
        calibInfo.ltop,
        calibInfo.rtop,
        calibInfo.lbot,
        calibInfo.rbot,
        calibInfo.diameter,
        outputPath,
    )

    outputPath = os.path.join(
        projectPath, "./data/test-center/all-centers-before-rotate.png"
    )
    drawAllCenters(image, allCenterPoints, calibInfo.diameter, outputPath)


    input_folder = os.path.join(projectPath, './data/mini-garden')
    output_folder = os.path.join(projectPath, './data/mini-garden-rotate')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(60):  # 遍历 image000.bmp 到 image299.bmp
        image_name = f'Image{i:03d}.bmp'
        input_path = os.path.join(input_folder, image_name)
        
        if os.path.exists(input_path):
            raw_image = cv2.imread(input_path)
            image = raw_image
            rotatedImage, rotatedCenters = rotate(
                image, calibInfo.ltop, calibInfo.rtop, calibInfo.diameter, allCenterPoints
            )
            
            output_name = f'image{i:03d}.png'
            output_path = os.path.join(output_folder, output_name)
            cv2.imwrite(output_path, rotatedImage)
            # print(f'Saved: {output_path}')
        else:
            print(f'File not found: {input_path}')

    # - rotate and draw
    
    # cv2.imwrite(os.path.join(projectPath, "./data/rotate/before.png"), image)
    # cv2.imwrite(os.path.join(projectPath, "./data/rotate/after.png"), rotatedImage)

    # outputPath = os.path.join(
    #     projectPath, "./data/test-center/all-centers-after-rotate.png"
    # )
    # drawAllCenters(rotatedImage, rotatedCenters, calibInfo.diameter, outputPath)
