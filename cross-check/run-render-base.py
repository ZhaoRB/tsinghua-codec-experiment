import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from tasks.format_convert import img2yuv
from tasks.render import rlc_render

# parameters
frames = 300

max_workers = 8  # Set the maximum number of concurrent processes

doRender = True
doConvert = True  # output from rlc is images, decide weather convert to yuv

frames = 300
seqs = [
    "Boys",
    "MiniGarden",
    "HandTools",
    "NewMotherboard",
    "Matryoshka",
    "NagoyaFujita",
    "NagoyaOrigami",
]
rendered_resolutions = {
    "Boys": [1348, 980],
    "HandTools": [1370, 1004],
    "NewMotherboard": [1370, 1004],
    "MiniGarden": [1370, 1004],
    "Matryoshka": [1370, 1004],
    "NagoyaFujita": [888, 904],
    "NagoyaOrigami": [888, 904],
}

rlc = "./executable/RLC40"
ffmpeg = "./executable/ffmpeg"

inputFolder = "/home/data/mpeg148-sequences/"
outputFolder = "/home/data/mpeg148-anchor/render-base"
os.makedirs(outputFolder, exist_ok=True)

configFolder = "./config"


def getBaseRenderImageFolderPath(seq):
    filepath = os.path.join(outputFolder, seq)
    os.makedirs(filepath, exist_ok=True)
    return filepath


def getBaseRenderYuvPath(seq):
    return os.path.join(
        outputFolder,
        f"{seq}_{rendered_resolutions[seq][0]}x{rendered_resolutions[seq][1]}_{frames}frames_8bit_yuv420.yuv",
    )


def getRenderLogFilePath(seq):
    return os.path.join(outputFolder, f"{seq}.log")


def getRawImagePattern(seq):
    return os.path.join(inputFolder, seq, "Image%03d.png")


def run_task(seq, convertToYuv=True):
    print(f"Starting task for {seq}")
    start_time = time.time()  # Record start time

    log_file = getRenderLogFilePath(seq)

    # rlc render
    frame_pattern = os.path.join(getBaseRenderImageFolderPath(seq), "frame#%03d")
    rlc_cfg_path = os.path.join(configFolder, seq, "param.cfg")
    calib_path = os.path.join(configFolder, seq, "calib.xml")

    rlc_render(
        rlc,
        rlc_cfg_path,
        getRawImagePattern(seq),
        frame_pattern,
        calib_path,
        0,
        frames,
        5,
        log_file,
    )

    if convertToYuv:
        # render result, img2yuv
        rendered_image_pattern = os.path.join(frame_pattern, "image_013.png")
        img2yuv(
            ffmpeg,
            0,
            frames,
            rendered_image_pattern,
            getBaseRenderYuvPath(seq),
            log_file,
        )

    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    print(f"Task for {seq} completed in {duration:.2f} seconds.")


with ProcessPoolExecutor(max_workers=max_workers) as executor:
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
