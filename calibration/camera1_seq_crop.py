import os

import cv2
import numpy as np
from center.draw_center import drawCenters
from parse_xml.parse import parseCalibXmlFile, updateCalibInfo
from rotateAndCrop.crop import calCropPos, crop

if __name__ == "__main__":
    # - set path
    projectPath = "/home/zrb/project/tsinghua-codec-experiment"
    name = "minigarden"
    seq_name = "handtools"
    seq_full_name = "HandTools_0925"

    calibrationFilePath = os.path.join(projectPath, f"./cfg/test/{name}.xml")
    inputPath = os.path.join(projectPath, f"./data/sample/{seq_name}.bmp")
    image = cv2.imread(inputPath)

    # output path
    fourCenterPath = os.path.join(projectPath, f"./data/center/four_{seq_name}.png")
    rotatePath = os.path.join(
        projectPath, f"./data/cropAndRotate/rotate_{seq_name}.bmp"
    )
    cropAndRotatePath = os.path.join(
        projectPath, f"./data/cropAndRotate/cropAndRotate_{seq_name}.bmp"
    )
    newCalibPath = os.path.join(projectPath, f"./cfg/test/new_{name}.xml")

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

    # - process one image
    ltop = calibInfo.ltop
    rtop = calibInfo.rtop
    lbot = calibInfo.lbot
    rbot = calibInfo.rbot

    ltopX, ltopY, rbotX, rbotY = calCropPos(
        ltop, lbot, rtop, rbot, calibInfo.diameter, False
    )
    rotated_cropped_image = crop(image, ltopX, ltopY, rbotX, rbotY)

    cv2.imwrite(cropAndRotatePath, rotated_cropped_image)

    # update calibration file
    ltop[0] = ltop[0] - ltopX
    rtop[0] = rtop[0] - ltopX
    lbot[0] = lbot[0] - ltopX
    rbot[0] = rbot[0] - ltopX

    ltop[1] = ltop[1] - ltopY
    rtop[1] = rtop[1] - ltopY
    lbot[1] = lbot[1] - ltopY
    rbot[1] = rbot[1] - ltopY

    updateCalibInfo(ltop, rtop, lbot, rbot, calibrationFilePath, newCalibPath)

    # 测试旋转之后的图片和4个中心点是否能对应上
    drawCenters(
        rotated_cropped_image.copy(),
        np.array([ltop, rtop, lbot, rbot]),
        calibInfo.diameter,
        os.path.join(projectPath, f"./data/center/processed_four_{seq_name}.png"),
    )

    # - process all
    seq_input_path = f"/data/MPEG148_TSPC_Sequences/{seq_full_name}"
    seq_output_path_bmp = (
        f"/data/MPEG148_TSPC_Sequences/{seq_full_name}_rotateAndCrop_bmp"
    )
    seq_output_path_png = (
        f"/data/MPEG148_TSPC_Sequences/{seq_full_name}_rotateAndCrop_png"
    )

    for i in range(301):
        image_name = f"Image{i:03d}.bmp"
        input_path = os.path.join(seq_input_path, image_name)

        if os.path.exists(input_path):
            raw_image = cv2.imread(input_path)

            # - process and save
            processed_image = crop(image, ltopX, ltopY, rbotX, rbotY)

            output_name = f"Image{i:03d}.bmp"
            output_path = os.path.join(seq_output_path_bmp, output_name)
            cv2.imwrite(output_path, processed_image)

            output_name = f"Image{i:03d}.png"
            output_path = os.path.join(seq_output_path_png, output_name)
            cv2.imwrite(output_path, processed_image)

            print(f"Saved: {output_path}")
        else:
            print(f"File not found: {input_path}")
