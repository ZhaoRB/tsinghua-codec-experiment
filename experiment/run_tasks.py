import argparse
import tomllib

from tasks.format_convert import img2yuv, yuv2img


def parseConfigFile():
    parser = argparse.ArgumentParser(description="Parse toml configuration file")
    parser.add_argument("toml_file", help="Path to the toml configuration file")
    args = parser.parse_args()

    with open(args.toml_file, "rb") as toml_file:
        config = tomllib.load(toml_file)

    return config


def run():
    config = parseConfigFile()

    for task in config["task"]["tasks"]:
        func = globals().get(task)  # 从全局作用域获取函数
        if func:
            func()  
        else:
            print(f"Function {task} not found!")


if __name__ == "__main__":
    run()
