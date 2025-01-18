from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class SeqInfo:
    width: int
    height: int
    diameter: float
    ltop: np.ndarray
    rtop: np.ndarray
    lbot: np.ndarray
    rbot: np.ndarray
    isVertical: bool
    rowNum: int
    colNum: int
    allCenterPoints: np.ndarray

    def hasAnotherColumn(self):
        # print(self.width, self.rtop[0], self.diameter)
        return (self.width - self.rtop[0]) > self.diameter

    def calRowAndColNum(self):
        # if self.isVertical:
        self.rowNum = round((self.lbot[1] - self.ltop[1]) / self.diameter) + 1
        self.colNum = round(
            (self.rtop[0] - self.ltop[0]) / (self.diameter / 2 * np.sqrt(3)) + 1
        )
        # print(self.rowNum)
        if self.hasAnotherColumn():
            self.colNum += 1
        else:
            self.rowNum -= 1
        # else:
        #     self.rowNum = round(
        #         (self.lbot[1] - self.ltop[1]) / self.diameter / 2 * np.sqrt(3) + 1
        #     )
        #     self.colNum = round((self.rtop[0] - self.ltop[0]) / self.diameter + 1)

    def calAllCenters(self):
        self.allCenterPoints = np.zeros((self.rowNum, self.colNum, 2))

        gapNum = self.colNum - 2 if self.hasAnotherColumn() else self.colNum - 1
        distance_col = (self.rtop - self.ltop) / gapNum

        for col in range(self.colNum):
            ratioL = (self.colNum - 1 - col) / (self.colNum - 1)
            ratioR = col / (self.colNum - 1)

            gapNum = self.rowNum - 1 if self.hasAnotherColumn() else self.rowNum
            distance_row = (
                ratioL * (self.lbot - self.ltop) + ratioR * (self.rbot - self.rtop)
            ) / gapNum

            firstPoint = self.ltop + distance_col * col
            if col % 2 == 1:
                firstPoint = firstPoint + distance_row / 2
            self.allCenterPoints[0, col] = firstPoint

            for row in range(self.rowNum - 1):
                cur = row + 1
                self.allCenterPoints[cur, col] = (
                    self.allCenterPoints[cur - 1, col] + distance_row
                )

    def calibAllCenters(self):
        for col in range(self.colNum):
            for row in range(self.rowNum):
                self.allCenterPoints[row, col, 0] = int(
                    round(self.allCenterPoints[row, col, 0])
                )
                self.allCenterPoints[row, col, 1] = int(
                    round(self.allCenterPoints[row, col, 1])
                )
        for row in range(self.rowNum):
            odd_cols = self.allCenterPoints[row, ::2, 1]
            mode_odd_y = stats.mode(odd_cols, keepdims=False)[0]
            if mode_odd_y % 2 == 1:
                mode_odd_y += 1
            self.allCenterPoints[row, ::2, 1] = mode_odd_y

            even_cols = self.allCenterPoints[row, 1::2, 1]
            mode_even_y = stats.mode(even_cols, keepdims=False)[0]
            if mode_even_y % 2 == 1:
                mode_even_y += 1
            self.allCenterPoints[row, 1::2, 1] = mode_even_y

        for col in range(self.colNum):
            x_coords = self.allCenterPoints[:, col, 0]
            mode_x = stats.mode(x_coords, keepdims=False)[0]
            if mode_x % 2 == 1:
                mode_x += 1
            self.allCenterPoints[:, col, 0] = mode_x


@dataclass
class TaskInfo:
    inputFile: str
    outputFiles: list[str]
    framesToBeEncoded: int
