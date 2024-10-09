import tomllib
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Task:
    start_frame: int
    frames: int
    sequences: List[str]
    vtm_types: List[str]
    qps: Dict[str, List[int]]
    tasks: List[str]
    img_pattern: str


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
    raw: List[int]
    mca: List[int]
    mca20: List[int]


@dataclass
class Config:
    task: Task
    path: Path
    vtm: VTM
    rlc: RLC
    resolutions: Dict[str, Resolution]


def parseConfigFile(cfg_file) -> Config:
    with open(cfg_file, "rb") as toml_file:
        toml_config = tomllib.load(toml_file)

    task = (
        Task(
            frames=toml_config["task"]["frame"],
            start_frame=toml_config["task"]["start_frame"],
            img_pattern=toml_config["task"]["img_pattern"],
            sequences=toml_config["task"]["sequences"],
            vtm_types=toml_config["task"]["vtm_types"],
            tasks=toml_config["task"]["tasks"],
            qps=toml_config["qps"],
        ),
    )
    path = (
        Path(
            input_folder=toml_config["path"]["input"],
            output_folder=toml_config["path"]["output"],
        ),
    )
    vtm = (
        VTM(
            ConformanceMode=toml_config["vtm"]["ConformanceMode"],
        ),
    )
    rlc = (RLC(views=toml_config["rlc"]["views"]),)
    resolutions = {}

    return Config(task, path, vtm, rlc, resolutions)
