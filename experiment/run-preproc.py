import argparse
import concurrent.futures
import tomllib

from tasks.format_convert import img_yuv_convert
from tasks.mca import mca

parser = argparse.ArgumentParser(description="Parse toml configuration file")
parser.add_argument("toml_file", help="Path to the toml configuration file")
args = parser.parse_args()

with open(args.toml_file, "rb") as toml_file:
    config = tomllib.load(toml_file)


def run(seq, tool):
    filename, mca_width, mca_height = mca(config, f"{tool}_pre", seq)

    config.update({f"{tool}_res": [mca_width, mca_height]})

    img_yuv_convert("img2yuv", config, filename, mca_width, mca_height)


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for seq in config["task"]["sequences"]:
            for tool in config["task"]["lvc_tools"]:
                futures.append(executor.submit(run, seq, tool))
