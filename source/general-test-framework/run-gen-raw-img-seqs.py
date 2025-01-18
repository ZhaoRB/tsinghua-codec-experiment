import sys
import time

from initialize import *
from tasks.format_convert import yuv2img


def run_task(seq):
    print(f"Convert raw yuv sequence {seq} to image sequence")
    start_time = time.time()  # Record start time

    # ========================= start =========================
    os.makedirs(getRawImageFolder(seq), exist_ok=True)
    os.chmod(getRawImageFolder(seq), 0o777)

    width, height = resolutions[seq]

    yuv2img(
        ffmpeg,
        width,
        height,
        getRawYuvPath(seq),
        getRawImagePattern(seq),
    )
    # ========================= end =========================

    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Task for {seq} completed in {int(hours)}h {int(minutes)}m {seconds:.2f}s.")


if __name__ == "__main__":
    for seq in seqs:
        run_task(seq)
