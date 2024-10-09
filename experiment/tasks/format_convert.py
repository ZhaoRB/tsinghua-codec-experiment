import subprocess


def img2yuv(app_ffmpeg, input, output, startFrame, frames):
    # subprocess.run(
    #     [
    #         app_ffmpeg,
    #         "-start_number",
    #         startFrame,
    #         "-i",
    #         input,
    #         "-vf",
    #         "format=yuv420p",
    #         "-frames:v",
    #         frames,
    #         output,
    #         "-y",  # 自动覆盖已存在的输出文件，不进行确认。
    #     ]
    # )
    print("img2yuv")


def yuv2img(app_ffmpeg, input, output, width, height):
    # subprocess.run(
    #     [
    #         app_ffmpeg,
    #         "-s",
    #         f"{width}x{height}",
    #         "-pix_fmt",
    #         "yuv420p",
    #         "-i",
    #         input,
    #         output,
    #         "-y",  # 自动覆盖已存在的输出文件，不进行确认。
    #     ]
    # )
    print("yuv2img")
