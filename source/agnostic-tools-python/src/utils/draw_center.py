import cv2
import numpy as np


def draw_centers(image: np.ndarray, points: np.ndarray, diameter, outputPath):
    print(points.shape)  # shape is (42, 49, 2)
    color = (0, 0, 255)
    Thickness = 2

    for row in range(points.shape[0]):
        for col in range(points.shape[1]):
            cv2.circle(
                image,
                (int(points[row, col, 0]), int(points[row, col, 1])),
                int(diameter // 2),
                color,
                Thickness,
            )

    cv2.imwrite(outputPath, image)

    return image
