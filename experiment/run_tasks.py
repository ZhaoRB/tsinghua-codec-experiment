import argparse

from config import parseConfigFile


def run():
    parser = argparse.ArgumentParser(description="Parse toml configuration file")
    parser.add_argument("toml_file", help="Path to the toml configuration file")
    args = parser.parse_args()

    config = parseConfigFile(args.toml_file)


if __name__ == "__main__":
    run()
        
