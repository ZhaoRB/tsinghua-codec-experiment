from dataclasses import dataclass


@dataclass
class Task:
    frames: int
    sequences: list[str]
    vtm_types: list[str]
    tasks: list[str]
    qps: dict[str, list[int]]


@dataclass
class Path:
    input_folder: str
    output_folder: str


@dataclass
class VTM:
    ConformanceMode: int


@dataclass
class RLC:
    views: int


@dataclass
class Resolution:
    raw: list
    mca: list
    mca20: list


@dataclass
class Config:
    task: Task
    path: Path
    vtm: VTM
    rlc: RLC
    resolutions: dict[str, Resolution]
