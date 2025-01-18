import argparse
import os

import cv2
from parse_xml.parse import parseCalibXmlFile, updateCalibInfo
from rotateAndCrop.crop import calCropPos, crop

if __name__ == "__main__":
    # - set path
    projectPath = "/home/zrb/project/tsinghua-codec-experiment"

    parser = argparse.ArgumentParser(description="Process some filenames.")

    parser.add_argument("name", help="The first filename")
    parser.add_argument("seqName", help="The second filename")

    args = parser.parse_args()

    name = args.name
    seqName = args.seqName

    # - parse calibration file and calulate center points
    calibrationFilePath = f"{projectPath}/cfg/1007/{name}.xml"
    calibInfo = parseCalibXmlFile(calibrationFilePath)

    # - calculate crop params, update calibration file
    ltop = calibInfo.ltop
    rtop = calibInfo.rtop
    lbot = calibInfo.lbot
    rbot = calibInfo.rbot

    ltopX, ltopY, rbotX, rbotY = calCropPos(
        ltop, lbot, rtop, rbot, calibInfo.diameter, False
    )

    # update calibration file
    ltop[0] = ltop[0] - ltopX
    rtop[0] = rtop[0] - ltopX
    lbot[0] = lbot[0] - ltopX
    rbot[0] = rbot[0] - ltopX

    ltop[1] = ltop[1] - ltopY
    rtop[1] = rtop[1] - ltopY
    lbot[1] = lbot[1] - ltopY
    rbot[1] = rbot[1] - ltopY

    newCalibPath = f"{projectPath}/cfg/1007/cropped_{name}.xml"
    updateCalibInfo(ltop, rtop, lbot, rbot, calibrationFilePath, newCalibPath)

    # - process all
    seqPath = "/home/data/1007restore"
    seq_input_path = f"{seqPath}/{seqName}"
    seq_output_path = f"{seqPath}/cropped_{seqName}"
    if not os.path.exists(seq_output_path):
        os.makedirs(seq_output_path)

    for i in range(301):
        image_name = f"Image{i:03d}.bmp"
        input_path = os.path.join(seq_input_path, image_name)

        if os.path.exists(input_path):
            raw_image = cv2.imread(input_path)

            # - process and save
            processed_image = crop(raw_image, ltopX, ltopY, rbotX, rbotY)

            output_name = f"Image{i:03d}.png"
            output_path = os.path.join(seq_output_path, output_name)
            cv2.imwrite(output_path, processed_image)

            print(f"Saved: {output_path}")
        else:
            print(f"File not found: {input_path}")
