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

