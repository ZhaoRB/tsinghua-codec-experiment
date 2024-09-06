import xml.etree.ElementTree as ET

import cv2
import numpy as np

def drawCenters(image: np.ndarray, points: np.ndarray, diameter, outputPath):
    color = (0, 0, 255)
    Thickness = 2
    
    for point in points:
        if point.shape[0] == 0:
            continue
        center = (round(point[0]), round(point[1]))
        cv2.circle(image, center, diameter // 2, color, Thickness)

    cv2.imwrite(outputPath, image)


if __name__ == "__main__":
    calibrationFilePath = (
        "/Users/riverzhao/Project/Codec/0_lvc_codec/Inter-MCA/config/new-seq/tlct.xml"
    )
    imageFilePath = (
        "/Users/riverzhao/Project/Codec/0_lvc_codec/Inter-MCA/data/raw/miniGarden.bmp"
    )

    image = cv2.imread(imageFilePath)
    output_path = "/Users/riverzhao/Project/Codec/0_lvc_codec/Inter-MCA/data/center/new-seq/three-points.png"
