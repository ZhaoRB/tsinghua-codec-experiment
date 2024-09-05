import xml.etree.ElementTree as ET

import numpy as np
from parse_xml.data_structure import CalibInfo
import math


def parseCalibXmlFile(calibrationFilePath) -> CalibInfo:
    tree = ET.parse(calibrationFilePath)
    root = tree.getroot()

    diameterNode = root.find("diameter")
    diameter = int(diameterNode.text)
    centersNode = root.find("centers")

    points = []
    for name in ["ltop", "rtop", "lbot", "rbot"]:
        points.append(
            np.array(
                [
                    float(centersNode.find(name).find("x").text),
                    float(centersNode.find(name).find("y").text),
                ]
            )
        )
    
    [ltop, rtop, lbot, rbot] = points

    rowNum = round((lbot[1] - ltop[1]) / diameter) + 1
    colNum = round((rtop[0] - ltop[0]) / diameter / math.sqrt(3) + 1) * 2

    return CalibInfo(
        diameter, rowNum, colNum, ltop, rtop, lbot, rbot
    )
