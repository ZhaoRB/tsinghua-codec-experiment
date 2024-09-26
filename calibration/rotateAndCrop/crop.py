"""
Rotate TSPC lenslet images
"""

import math

import cv2
import numpy as np


def calCropPos(ltop, lbot, rtop, rbot, diameter, isBoys: bool):
    ltopX = math.floor(
        min(
            ltop[0] - diameter / 2,
            lbot[0] - diameter / 2,
        )
    )
    ltopY = math.floor(
        min(
            ltop[1] - diameter / 2,
            rtop[1] - diameter / 2,
        )
    )
    biasX = diameter / 2 if isBoys else (diameter / 2 * (math.sqrt(3) + 1))
    biasY = diameter / 2 if isBoys else diameter
    rbotX = math.ceil(max(rtop[0] + biasX, rbot[0] + biasX))
    rbotY = math.ceil(max(lbot[1] + biasY, rbot[1] + biasY))
    print(ltopX, ltopY, rbotX, rbotY)

    return [ltopX, ltopY, rbotX, rbotY]


def crop(image, ltopX, ltopY, rbotX, rbotY):
    if (rbotX - ltopX) % 2 == 1:
        rbotX = rbotX + 1
    if (rbotY - ltopY) % 2 == 1:
        rbotY = rbotY - 1
    cropped_image = image[ltopY:rbotY, ltopX:rbotX]
    return cropped_image
