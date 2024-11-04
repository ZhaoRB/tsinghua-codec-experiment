import cv2
from center.cal_center import calculateAllCenters
from center.draw_center import drawCenters
from parse_xml.parse import parseCalibXmlFile, updateCalibInfo
from rotateAndCrop.crop import calCropPos, crop

# - set path
calibFolder = "/home/zrb/project/tsinghua-codec-experiment/cfg"
imageFolder = "/home/zrb/project/tsinghua-codec-experiment/data"
seqName = "Matryoshka"

image = cv2.imread(f"{imageFolder}/sample/{seqName}.bmp")

# - parse calibration file and calulate center points
calibrationFilePath = f"{calibFolder}/{seqName}.xml"
calibInfo = parseCalibXmlFile(calibrationFilePath)
allCenterPoints = calculateAllCenters(calibInfo)

# - draw
drawCenters(
    image.copy(),
    allCenterPoints.reshape(allCenterPoints.shape[0] * allCenterPoints.shape[1], 2),
    calibInfo.diameter,
    f"{imageFolder}/center/center_{seqName}.png",
)

# - calculate crop params, update calibration file
ltop = calibInfo.ltop
rtop = calibInfo.rtop
lbot = calibInfo.lbot
rbot = calibInfo.rbot

ltopX, ltopY, rbotX, rbotY = calCropPos(
    ltop, lbot, rtop, rbot, calibInfo.diameter, False
)

# update calibration file
ltop[0] = ltop[0] - ltopX
rtop[0] = rtop[0] - ltopX
lbot[0] = lbot[0] - ltopX
rbot[0] = rbot[0] - ltopX

ltop[1] = ltop[1] - ltopY
rtop[1] = rtop[1] - ltopY
lbot[1] = lbot[1] - ltopY
rbot[1] = rbot[1] - ltopY

newCalibPath = f"{calibFolder}/cropped_{seqName}.xml"
updateCalibInfo(ltop, rtop, lbot, rbot, calibrationFilePath, newCalibPath)

calibInfo = parseCalibXmlFile(newCalibPath)
allCenterPoints = calculateAllCenters(calibInfo)

# - crop

croppedImage = crop(image, ltopX, ltopY, rbotX, rbotY)
cv2.imwrite(f"{imageFolder}/cropAndRotate/cropped_{seqName}.png", croppedImage)

drawCenters(
    croppedImage.copy(),
    allCenterPoints.reshape(allCenterPoints.shape[0] * allCenterPoints.shape[1], 2),
    calibInfo.diameter,
    f"{imageFolder}/center/center_cropped_{seqName}.png",
)
