import subprocess

from PIL import Image


def get_image_resolution(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height


def img2yuv(ffmpeg, input, output, frames=1, startFrame=1):
    imagePattern = "Image%03d.png"

    subprocess.run(
        [
            ffmpeg,
            "-start_number",
            startFrame,
            "-i",
            f"{input}/{imagePattern}",
            "-vf",
            "format=yuv420p",
            "-frames:v",
            frames,
            output,
            "-y",
        ]
    )


def yuv2img(ffmpeg, input, output, width, height):
    subprocess.run(
        [
            ffmpeg,
            "-s",
            f"{width}x{height}",
            "-pix_fmt",
            "yuv420p",
            "-i",
            input,
            output,
            "-y",
        ]
    )
