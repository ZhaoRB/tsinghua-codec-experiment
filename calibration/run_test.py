import cv2
from center.draw_center import drawCornerCenters
from parse_xml.parse import parseCalibXmlFile
from rotate.rotate import rotate

if __name__ == "__main__":
    calibFilePath = (
        "/home/zrb/project/tsinghua-codec-experiment/cfg/test/minigarden.xml"
    )
    calibInfo = parseCalibXmlFile(calibFilePath)

    print(calibInfo)

    img_name = "MiniGarden"
    inputPath = (
        f"/home/zrb/project/tsinghua-codec-experiment/data/sample/{img_name}.png"
    )
    img = cv2.imread(inputPath)

    # Draw corner centers on the image
    # outputPath = f"/home/zrb/project/tsinghua-codec-experiment/data/img-with-center/{img_name}_four_centers.png"
    # drawCornerCenters(
    #     img,
    #     calibInfo.ltop,
    #     calibInfo.rtop,
    #     calibInfo.lbot,
    #     calibInfo.rbot,
    #     calibInfo.diameter,
    #     outputPath
    # )

    # rotate image
    rotatedImage = rotate(
        img, calibInfo.ltop, calibInfo.rtop, calibInfo.lbot, calibInfo.rbot
    )
