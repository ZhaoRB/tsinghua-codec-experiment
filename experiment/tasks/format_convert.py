import subprocess


def img2yuv(app_ffmpeg, input, output, frames=1, startFrame=1):
    imagePattern = "Image%03d.png"

    subprocess.run(
        [
            app_ffmpeg,
            "-start_number",
            startFrame,
            "-i",
            f"{input}/{imagePattern}",
            "-vf",
            "format=yuv420p",
            "-frames:v",
            frames,
            output,
            "-y",  # 自动覆盖已存在的输出文件，不进行确认。
        ]
    )


def yuv2img(app_ffmpeg, input, output, width, height):
    subprocess.run(
        [
            app_ffmpeg,
            "-s",
            f"{width}x{height}",
            "-pix_fmt",
            "yuv420p",
            "-i",
            input,
            output,
            "-y",  # 自动覆盖已存在的输出文件，不进行确认。
        ]
    )
