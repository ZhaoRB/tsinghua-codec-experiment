import argparse
import tomllib

from tasks.codec import vvc_codec
from tasks.format_convert import img2yuv
from tasks.mca import mca
# from utils.utils import update_config

parser = argparse.ArgumentParser(description="Parse toml configuration file")
parser.add_argument("toml_file", help="Path to the toml configuration file")
args = parser.parse_args()

with open(args.toml_file, "rb") as toml_file:
    config = tomllib.load(toml_file)


def run(seq, tool):
    mca_width, mca_height = mca()
    config.update({f"{tool}_res": [mca_width, mca_height]})
    img2yuv()


if __name__ == "__main__":
    for seq in config["task"]["sequences"]:
        for tool in config["task"]["lvc_tools"]:
            run(seq, tool)
