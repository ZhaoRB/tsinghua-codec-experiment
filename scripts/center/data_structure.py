from dataclasses import dataclass

@dataclass
class CalibInfo:
    diameter: float
    rowNum: int
    colNum: int
    ltop: tuple
    rtop: tuple
    lbot: tuple
    rbot: tuple