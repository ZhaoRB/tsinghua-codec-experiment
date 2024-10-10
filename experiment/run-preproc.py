import argparse
import tomllib

from tasks.codec import *
from tasks.format_convert import *
from tasks.mca import *

parser = argparse.ArgumentParser(description="Parse toml configuration file")
parser.add_argument("toml_file", help="Path to the toml configuration file")
args = parser.parse_args()

with open(args.toml_file, "rb") as toml_file:
    config = tomllib.load(toml_file)


def run():
    for seq in config["task"]["sequences"]:
        mca_width, mca_height = mca_pre()


if __name__ == "__main__":
    run()
