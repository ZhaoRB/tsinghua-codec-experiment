import argparse
import tomllib
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


# @dataclass
# class Config:
#     task: Task
#     path: Path
#     vtm: VTM
#     rlc: RLC
#     resolutions: dict[str, Resolution]


def parseConfigFile():
    parser = argparse.ArgumentParser(description="Parse toml configuration file")
    parser.add_argument("toml_file", help="Path to the toml configuration file")
    args = parser.parse_args()

    with open(args.toml_file, "rb") as toml_file:
        toml_config = tomllib.load(toml_file)

    task = (
        Task(
            frames=toml_config["task"]["frame"],
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

    return task, path, vtm, rlc, resolutions
