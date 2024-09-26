import math
import xml.etree.ElementTree as ET

import numpy as np
from parse_xml.data_structure import CalibInfo


# four point version xml file
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

    return CalibInfo(diameter, rowNum, colNum, ltop, rtop, lbot, rbot)

def updateCalibInfo(ltop, rtop, lbot, rbot, oldPath, newPath):
    def update_node(x, y, node_name):
        node = centersNode.find(node_name)
        node.find("x").text = str(round(x, 1))
        node.find("y").text = str(round(y, 1))
    
    tree = ET.parse(oldPath)
    root = tree.getroot()

    centersNode = root.find("centers")

    update_node(ltop[0], ltop[1], "ltop")
    update_node(rtop[0], rtop[1], "rtop")
    update_node(lbot[0], lbot[1], "lbot")
    update_node(rbot[0], rbot[1], "rbot")

    tree.write(newPath)


# old version: three points xml file
def parseCalibXmlFileOld(calibrationFilePath) -> CalibInfo:
    tree = ET.parse(calibrationFilePath)
    root = tree.getroot()

    diameterNode = root.find("diameter")
    diameter = int(diameterNode.text)
    centersNode = root.find("centers")
    rowNode = centersNode.find("rows")
    rowNum = int(rowNode.text)
    colNode = centersNode.find("cols")
    colNum = int(colNode.text)

    ltop = np.array(
        [
            float(centersNode.find("ltop").find("x").text),
            float(centersNode.find("ltop").find("y").text),
        ]
    )
    rtop = np.array(
        [
            float(centersNode.find("rtop").find("x").text),
            float(centersNode.find("rtop").find("y").text),
        ]
    )
    lbot = np.array(
        [
            float(centersNode.find("lbot").find("x").text),
            float(centersNode.find("lbot").find("y").text),
        ]
    )

    rbot = np.array([])

    return CalibInfo(diameter, rowNum, colNum, ltop, rtop, lbot, rbot)
