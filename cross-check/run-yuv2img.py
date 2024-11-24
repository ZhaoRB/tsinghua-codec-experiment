import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from initialize import *
from tasks.codec import vvc_codec
from tasks.format_convert import yuv2img

codecLogFile = os.path.join(codecOutputFolder, "yuv2img.log")
seqs_toConvert = [
    "Boys",
    "HandTools",
    "MiniGarden2",
    "Motherboard2",
    "Matryoshka",
    "NagoyaFujita",
    "NagoyaOrigami"
]
qps_toConvert = {
    # subjective + objective
    "Boys": [36, 40, 44, 48],
    "HandTools": [34, 38, 42, 46, 50, 54],
    "MiniGarden2": [34, 38, 42, 46, 50, 54],
    "Motherboard2": [34, 38, 42, 46, 50],
    "NagoyaOrigami": [28, 32, 36, 40, 44, 48],
    # objective
    "Matryoshka": [40, 44, 48, 52],
    "NagoyaFujita": [36, 40, 44, 48],
}

def run_task(seq, qp):
    print(f"Starting convert for {seq} with QP {qp}...")
    start_time = time.time()  # Record start time

    # ========================= start =========================
    width, height = resolutions[seq]

    # codecLogFile = getCodecLogFilePath(seq, qp)
    # vvc_codec(
    #     encoder,
    #     getRawYuvPath(seq),
    #     getCodecYuvPath(seq, qp),
    #     os.path.join(configFolder, "vtm_RA.cfg"),
    #     width,
    #     height,
    #     frames,
    #     qp,
    #     codecLogFile,
    #     getBitstreamPath(seq, qp),
    # )

    yuv2img(
        ffmpeg,
        width,
        height,
        getCodecYuvPath(seq, qp),
        getCodecImagePattern(seq, qp),
        codecLogFile,
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
    for seq in seqs_toConvert:
        for qp in qps_toConvert[seq]:
            futures.append(executor.submit(run_task, seq, qp))

    for future in as_completed(futures):
        try:
            future.result()  # This will raise any exception that occurred in the process
        except Exception as e:
            print(f"An error occurred: {e}")
