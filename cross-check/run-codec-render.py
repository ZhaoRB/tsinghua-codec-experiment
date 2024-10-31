import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from initialize import *
from tasks.codec import vvc_codec
from tasks.format_convert import img2yuv, yuv2img
from tasks.render import rlc_render


def run_task(seq, qp):
    print(f"Starting task for {seq} with QP {qp}...")
    start_time = time.time()  # Record start time

    # ========================= start =========================
    width, height = resolutions[seq]

    # 1. vvc codec
    codecLogFile = getCodecLogFilePath(seq, qp)
    vvc_codec(
        encoder,
        getRawYuvPath(seq),
        getCodecYuvPath(seq, qp),
        os.path.join(configFolder, "vtm_RA.cfg"),
        width,
        height,
        frames,
        qp,
        codecLogFile,
    )

    # 2. ffmpeg yuv2img
    yuv2img(
        ffmpeg,
        width,
        height,
        getCodecYuvPath(seq, qp),
        getCodecImagePattern(seq, qp),
        codecLogFile,
    )

    # 3. rlc render
    rlc_cfg_path, calib_path = getRenderConfigPath(seq)
    renderLogFile = getRenderLogFilePath(seq, qp)

    rlc_render(
        rlc,
        rlc_cfg_path,
        getCodecImagePattern(seq, qp),
        getRenderFramePattern(seq, qp),
        calib_path,
        startFrame,
        frames,
        viewNum,
        renderLogFile,
    )

    # 4. render result, img2yuv
    img2yuv(
        ffmpeg,
        startFrame,
        frames,
        getRenderFramePattern(seq, qp),
        getRenderYuvPath(seq, qp),
        renderLogFile,
    )

    # ========================= end =========================

    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(
        f"Task for {seq} with QP {qp} completed in {int(hours)}h {int(minutes)}m {seconds:.2f}s."
    )


with ProcessPoolExecutor(max_workers=max_workers) as executor:
    futures = []
    for seq in seqs:
        for qp in qps[seq]:
            futures.append(executor.submit(run_task, seq, qp))

    for future in as_completed(futures):
        try:
            future.result()  # This will raise any exception that occurred in the process
        except Exception as e:
            print(f"An error occurred: {e}")
