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
