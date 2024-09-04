import os

import numpy as np
import cv2

whiteImagePath = "./whiteImage/0.2m.bmp"
colNum, rowNum = 66, 43
width, height = 4080, 3068

def getVignettingMatrix(): 
    whiteImage = cv2.imread(whiteImagePath)
    grayImage = cv2.cvtColor(whiteImage, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("whiteImage", whiteImage)
    # cv2.imshow("grayImage", grayImage)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    getVignettingMatrix()
