import argparse
import tomllib

import config
from tasks.codec import vvc_codec
from tasks.format_convert import img2yuv, yuv2img
from tasks.mca import mca20_post, mca20_pre, mca_post, mca_pre
from tasks.render import rlc_render


def parseConfigFile():
    parser = argparse.ArgumentParser(description="Parse toml configuration file")
    parser.add_argument("toml_file", help="Path to the toml configuration file")
    args = parser.parse_args()

    with open(args.toml_file, "rb") as toml_file:
        toml_config = tomllib.load(toml_file)

    cfg = config.Config(
        task=config.Task(
            frames=toml_config["task"]["frame"],
            sequences=toml_config["task"]["sequences"],
            vtm_types=toml_config["task"]["vtm_types"],
            tasks=toml_config["task"]["tasks"],
            qps=toml_config["qps"],
        ),
        path=config.Path(
            input_folder=toml_config["path"]["input"],
            output_folder=toml_config["path"]["output"],
        ),
        vtm=config.VTM(
            ConformanceMode=toml_config["vtm"]["ConformanceMode"],
        ),
        rlc=config.RLC(views=toml_config["rlc"]["views"]),
        resolutions={},
    )

    return cfg


def run():
    cfg = parseConfigFile()
    for seq in cfg.task.sequences:
        for vtm_type in cfg.task.vtm_types:
            pass


if __name__ == "__main__":
    run()
