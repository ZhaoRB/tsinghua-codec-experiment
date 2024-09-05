"""
Rotate TSPC lenslet images
"""

import math

import cv2
import numpy as np


# todo: 原理？
# calculate rotate angle from three points calibration file
def rotate(
    image: np.ndarray,
    ltop: np.ndarray,
    rtop: np.ndarray,
    lbot: np.ndarray,
    rbot: np.ndarray,
):
    vec1 = rtop - ltop + rbot - lbot
    vec1 = vec1 / np.linalg.norm(vec1)

    vec2 = lbot - ltop + rbot - rtop
    vec2 = vec2 / np.linalg.norm(vec2)
    # rotate90 = np.array([[0, 1], [-1, 0]])
    # vec2 = vec2 @ rotate90

    vec = vec1 + vec2

    angle = math.degrees(math.atan2(vec[1], vec[0]))

    print(f"vector: {vec}, rotation angle: {angle}")

    (h, w) = image.shape[:2]
    imgCenter = (w // 2, h // 2)

    # rotate matrix
    M = cv2.getRotationMatrix2D(imgCenter, angle, 1.0)

    rotated_image = cv2.warpAffine(image, M, (w, h))
    print(rotated_image.shape)

    # rotate center points

    return rotated_image


if __name__ == "__main__":
    img = cv2.imread(
        "/home/zrb/project/tsinghua-codec-experiment/data/sample/MiniGarden.png"
    )
    ltop = np.array([45.25, 37.5])
    rtop = np.array([4006.75, 70.75])
    diameter = 70

    rotatedImage = rotate(img, ltop, rtop)

    cv2.imwrite(
        "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment/data/rotate/rotate-garden.bmp",
        rotatedImage,
    )