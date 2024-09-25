"""
Rotate TSPC lenslet images
"""

import math

import cv2
import numpy as np


def calCropPos(ltop, lbot, rtop, rbot, diameter):
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
    rbotX = math.ceil(
        max(
            rtop[0] + diameter / 2 * (math.sqrt(3) + 1),
            rbot[0] + diameter / 2 * (math.sqrt(3) + 1),
        )
    )
    rbotY = math.ceil(max(lbot[1] + diameter, rbot[1] + diameter))
    print(ltopX, ltopY, rbotX, rbotY)

    return [ltopX, ltopY, rbotX, rbotY]


def crop(image, ltopX, ltopY, rbotX, rbotY):
    cropped_image = image[ltopY:rbotY, ltopX:rbotX]
    return cropped_image