import os

from PIL import Image


def make_dir(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)
        os.mkdir(dir)


def get_image_path(path, pattern, num):
    file_name = pattern % num
    full_path = os.path.join(path, file_name)
    return full_path


def get_image_res(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height


def set_seq_resolution(config: dict, seq: str, filename: str):
    input_folder = config["task"]["input_folder"]
    image_pattern = config["task"]["image_pattern"]
    start_frame = config["task"]["start_frame"]

    input_path = get_image_path(f"{input_folder}/{seq}", image_pattern, start_frame)
    width, height = get_image_res(input_path)
    config[seq]["res"] = [width, height]

    input_path = get_image_path(
        f"{input_folder}/{filename}", image_pattern, start_frame
    )
    width, height = get_image_res(input_path)
    tool = filename.split("_")[1]
    config[seq][f"{tool}_res"] = [width, height]
