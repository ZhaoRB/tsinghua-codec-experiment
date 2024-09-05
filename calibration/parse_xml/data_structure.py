from dataclasses import dataclass

import numpy as np


@dataclass
class CalibInfo:
    diameter: float
    rowNum: int
    colNum: int
    ltop: np.ndarray
    rtop: np.ndarray
    lbot: np.ndarray
    rbot: np.ndarray
