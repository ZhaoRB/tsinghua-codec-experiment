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
    diameter,
    centerPoints: np.ndarray,
):
    xBias = diameter / 2 * math.sqrt(3)
    yBias = diameter / 2

    ltopOdd = np.array([ltop[0] + xBias, ltop[1] + yBias])

    vec = rtop - ltopOdd
    print(f"ltop: {ltop}")
    print(f"rtop: {rtop}")
    print(f"ltopOdd: {ltopOdd}")
    angle = math.degrees(math.atan2(vec[1], vec[0]))

    print(f"vector: {vec} \nrotate angle: {angle}")

    (h, w) = image.shape[:2]
    imgCenter = (w // 2, h // 2)

    # rotate matrix
    M = cv2.getRotationMatrix2D(imgCenter, angle, 1.0)
    print(f"rotate matrix shape: {M.shape}")
    print(M[:, 0], M[:, 1], M[:, 2])

    rotated_image = cv2.warpAffine(image, M, (w, h))
    print(rotated_image.shape)

    # rotate center points
    m, n, _ = centerPoints.shape
    points_reshaped = centerPoints.reshape(-1, 2)

    ones = np.ones((points_reshaped.shape[0], 1))
    points_homogeneous = np.hstack((points_reshaped, ones))

    rotated_points_homogeneous = M @ points_homogeneous.T
    rotated_points = rotated_points_homogeneous[:2, :].T

    rotated_points_reshaped = rotated_points.reshape(m, n, 2)

    print(f"rotated right ltop: {rotated_points_reshaped[0, 0, :]}")
    print(f"rotated right rtop: {rotated_points_reshaped[0, n - 1, :]}")

    return rotated_image, rotated_points_reshaped


if __name__ == "__main__":
    img = cv2.imread(
        "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment/data/mini-garden/Image001.bmp"
    )
    ltop = np.array([45.25, 37.5])
    rtop = np.array([4006.75, 70.75])
    diameter = 70

    rotatedImage = rotate(img, ltop, rtop, diameter)

    cv2.imwrite(
        "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment/data/rotate/rotate-garden.bmp",
        rotatedImage,
    )
