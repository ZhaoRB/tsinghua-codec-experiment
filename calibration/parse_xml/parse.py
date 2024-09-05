import xml.etree.ElementTree as ET

import numpy as np
from data_structure import CalibInfo


def parseCalibXmlFile(calibrationFilePath) -> CalibInfo:
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

    if centersNode.find("rbot") is not None:
        rbot = np.array(
            [
                float(centersNode.find("rbot").find("x").text),
                float(centersNode.find("rbot").find("y").text),
            ]
        )
    else:
        rbot = np.array([])

    return CalibInfo(diameter, rowNum, colNum, ltop, rtop, lbot, rbot)
