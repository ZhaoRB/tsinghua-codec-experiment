import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from initialize import *
from tasks.render import rlc_render


def run_task(seq):
    print(f"Starting render for {seq} base ...")
    start_time = time.time()  # Record start time

    # ========================= start =========================
    rlc_cfg_path, calib_path = getRenderConfigPath(seq)
    renderLogFile = getBaseRenderLogFilePath(seq)

    rlc_render(
        rlc,
        rlc_cfg_path,
        getRawImagePattern(seq),
        getBaseRenderFramePattern(seq),
        calib_path,
        startFrame,
        frames,
        viewNum,
        renderLogFile,
    )
    # ========================= end =========================

    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(
        f"Task for {seq} base completed in {int(hours)}h {int(minutes)}m {seconds:.2f}s."
    )


with ProcessPoolExecutor(max_workers=max_workers) as executor:
    futures = []
    for seq in seqs:
        futures.append(executor.submit(run_task, seq))

    for future in as_completed(futures):
        try:
            future.result()  # This will raise any exception that occurred in the process
        except Exception as e:
            print(f"An error occurred: {e}")
