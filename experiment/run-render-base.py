import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from tasks.format_convert import img2yuv
from tasks.render import rlc_render

# parameters
inputFolder = "/home/data/mpeg148-tspc-seqs"
outputFolder = "/home/data/1021-tspc-multiQP-codec-render"
configFolder = "/home/zrb/project/tsinghua-codec-experiment/experiment/config"

frames = 30
seqs = ["NewMotherboard", "MiniGarden", "HandTools"]


def run_task(seq):
    print(f"Starting task for {seq}")
    start_time = time.time()  # Record start time

    log_file = os.path.join(outputFolder, f"{seq}_base.log")

    # width = 3976 if seq == "Boys" else 4036
    # height = 2956 if seq == "Boys" else 3064

    # rlc render
    input_images = os.path.join(inputFolder, seq, "Image%03d.png")
    output_render_folder = os.path.join(outputFolder, f"render-{seq}_base")
    output_render = os.path.join(outputFolder, f"render-{seq}_base", "frame#%03d")
    os.makedirs(output_render_folder, exist_ok=True)

    rlc = "/home/zrb/project/tsinghua-codec-experiment/experiment/executable/RLC40"
    rlc_cfg_path = os.path.join(configFolder, seq, "param.cfg")
    calib_path = os.path.join(configFolder, seq, "calib.xml")

    rlc_render(
        rlc,
        rlc_cfg_path,
        input_images,
        output_render,
        calib_path,
        0,
        frames,
        5,
        log_file,
    )

    # render result, img2yuv
    ffmpeg = "ffmpeg"

    rendered_width = 1348
    rendered_height = 980 if seq == "Boys" else 1004

    input_img2yuv = os.path.join(output_render, "image_013.png")
    output_render_yuv = os.path.join(
        outputFolder,
        f"render-{seq}_base_{rendered_width}x{rendered_height}_{frames}frames.yuv",
    )
    img2yuv(ffmpeg, 0, frames, input_img2yuv, output_render_yuv, log_file)

    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    print(f"Task for {seq} completed in {duration:.2f} seconds.")


with ProcessPoolExecutor(max_workers=16) as executor:
    futures = []
    for seq in seqs:
        futures.append(executor.submit(run_task, seq))

    for future in as_completed(futures):
        try:
            future.result()  # This will raise any exception that occurred in the process
        except Exception as e:
            print(f"An error occurred: {e}")


# for seq in seqs:
#     for qp in qps:
#         run_task(seq, qp)