import subprocess


def img_yuv_convert(type: str, config: dict, filename: str, width, height):
    ffmpeg = config["app"]["ffmpeg"]
    startFrame = config["task"]["start_frame"]
    frames = config["task"]["frames"]

    folder = config["task"]["output_folder"]
    image_pattern = config["task"]["image_pattern"]

    image_path = f"{folder}/{filename}/{image_pattern}"
    yuv_path = f"{folder}/{filename}-{width}x{height}-{frames}frames.yuv"

    cmds = (
        [
            ffmpeg,
            "-start_number",
            startFrame,
            "-i",
            image_path,
            "-vf",
            "format=yuv420p",
            "-frames:v",
            frames,
            yuv_path,
            "-y",
        ]
        if type == "img2yuv"
        else [
            ffmpeg,
            "-s",
            f"{width}x{height}",
            "-pix_fmt",
            "yuv420p",
            "-i",
            yuv_path,
            image_path,
            "-y",
        ]
    )
    subprocess.run(cmds)
