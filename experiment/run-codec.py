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


def run_pre(seq, tool):
    filename = mca(config, f"{tool}_pre", seq)
    

    img_yuv_convert("img2yuv", config, filename)

def run_codec():
    pass

def run_post():
    pass

def run_render():
    pass


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
        futures = []
        for seq in config["task"]["sequences"]:
            for tool in config["task"]["lvc_tools"]:
                futures.append(executor.submit(run_pre, seq, tool))
                for vtm_cfg in config["task"]["vtm_types"]:
                    for qp in config["qps"][seq]:
                        run_codec(vtm_cfg, qp)
