"""
Rotate TSPC lenslet images
"""

import math

import cv2
import numpy as np


# todo: 原理？
# calculate rotate angle from four points calibration file
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
    rotate90 = np.array([[0, 1], [-1, 0]])
    vec2 = rotate90 @ vec2

    vec = vec1 + vec2

    angle = math.degrees(math.atan2(vec[1], vec[0]))

    print(f"vector: {vec}, rotation angle: {angle}")

    (h, w) = image.shape[:2]
    imgCenter = (w // 2, h // 2)

    # rotate matrix
    M = cv2.getRotationMatrix2D(imgCenter, angle, 1.0)

    rotated_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR)
    print(rotated_image.shape)

    # rotate four points
    points = np.array([ltop, rtop, lbot, rbot])
    ones = np.ones((points.shape[0], 1))
    points_homogeneous = np.hstack([points, ones])  # Convert to homogeneous coordinates
    transformed_points = M @ points_homogeneous.T  # Apply the transformation
    transformed_points = transformed_points[:2, :].T  # Convert back to Cartesian coordinates

    return rotated_image, transformed_points
