import os
import time

from initialize import *
from tasks.format_convert import yuv2img


def run_task(seq, qp):
    print(f"Starting task for {seq} with QP {qp}...")
    start_time = time.time()  # Record start time

    # ========================= start =========================
    width, height = resolutions[seq]

    yuv2img(
        ffmpeg,
        width,
        height,
        getCodecYuvPath(seq, qp),
        getCodecImagePattern(seq, qp),
        os.path.join(codecOutputFolder, f"{seq}_qp{qp}.log"),
    )

    # ========================= end =========================

    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(
        f"Task for {seq} with QP {qp} completed in {int(hours)}h {int(minutes)}m {seconds:.2f}s."
    )


for seq in seqs:
    for qp in qps[seq]:
        run_task(seq, qp)
