import xml.etree.ElementTree as ET

import cv2
import numpy as np

calibrationFilePath = (
    "/Users/riverzhao/Project/Codec/0_lvc_codec/Inter-MCA/config/new-seq/tlct.xml"
)
imageFilePath = (
    "/Users/riverzhao/Project/Codec/0_lvc_codec/Inter-MCA/data/raw/miniGarden.bmp"
)

image = cv2.imread(imageFilePath)

tree = ET.parse(calibrationFilePath)
root = tree.getroot()

# 转换成float了，因为cv.circle
diameter = int(float(root.find("diameter").text))
centers = root.find("centers")

points = ["ltop", "rtop", "lbot"]
for point in points:
    x = float(centers.find(point).find("x").text)
    y = float(centers.find(point).find("y").text)
    cv2.circle(image, (int(x), int(y)), diameter // 2, (0, 0, 255), 2)

output_path = "/Users/riverzhao/Project/Codec/0_lvc_codec/Inter-MCA/data/center/new-seq/three-points.png"
cv2.imwrite(output_path, image)


def drawCornerCenters(image: np.ndarray, ltop, rtop, lbot, rbot, diameter):



# image_copy = image.copy()

# for row in allCenterPoints:
#     for point in row:
#         center = (round(point[0]), round(point[1]))
#         color = (0, 0, 255)
#         cv2.circle(image_copy, center, diameter // 2, color, 2)

# output_path = os.path.join(projectPath, "./data/center/all_center_cars.png")
# cv2.imwrite(output_path, image_copy)

# del image_copy


if __name__ == "__main__":
    pass