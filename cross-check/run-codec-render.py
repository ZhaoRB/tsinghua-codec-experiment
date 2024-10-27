import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from tasks.codec import vvc_codec
from tasks.format_convert import img2yuv, yuv2img
from tasks.render import rlc_render

# parameters
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
qps = {
    "Boys": [36, 40, 44, 48],
    "HandTools": [54, 50, 46, 42, 38, 34],
    "NewMotherboard": [54, 50, 46, 42, 38, 34],
    "MiniGarden": [54, 50, 46, 42, 38, 34],
    "Matryoshka": [40, 44, 48, 52, 56, 60],
    "NagoyaFujita": [24, 28, 32, 36, 40, 44],
    "NagoyaOrigami": [24, 28, 32, 36, 40, 44],
}
resolutions = {
    "Boys": [3976, 2956],
    "HandTools": [4036, 3064],
    "NewMotherboard": [4036, 3064],
    "MiniGarden": [4036, 3064],
    "Matryoshka": [4040, 3064],
    "NagoyaFujita": [2048, 2048],
    "NagoyaOrigami": [2048, 2048],
}

rendered_resolutions = {
    "Boys": [1348, 1004],
    "HandTools": [1370, 1004],
    "NewMotherboard": [1370, 1004],
    "MiniGarden": [1370, 1004],
    "Matryoshka": [1370, 1004],
    "NagoyaFujita": [888, 904],
    "NagoyaOrigami": [888, 904],
}

encoder = "./executable/EncoderAppStatic"
ffmpeg = "./executable/ffmpeg"
rlc = "./executable/RLC40-1025"

inputFolder = "/home/data/mpeg148-sequences"
outputFolder = "/home/data/mpeg148-anchor"
configFolder = "./config"

codecOutputFolder = os.path.join(outputFolder, "codec")
os.makedirs(codecOutputFolder, exist_ok=True)

renderOutputFolder = os.path.join(outputFolder, "render")
os.makedirs(renderOutputFolder, exist_ok=True)


def getCodecYuvPath(seq, qp):
    return os.path.join(
        codecOutputFolder,
        f"{seq}_{resolutions[seq][0]}x{resolutions[seq][1]}_qp{qp}_{frames}frames_8bit_yuv420.yuv",
    )


def getCodecImageFolderPath(seq, qp):
    filepath = os.path.join(codecOutputFolder, f"{seq}_qp{qp}")
    os.makedirs(filepath, exist_ok=True)
    return filepath


def getCodecLogFilePath(seq, qp):
    return os.path.join(codecOutputFolder, f"{seq}_qp{qp}.log")


def getRenderImageFolderPath(seq, qp):
    filepath = os.path.join(renderOutputFolder, f"{seq}_qp{qp}")
    os.makedirs(filepath, exist_ok=True)
    return filepath


def getRenderYuvPath(seq, qp):
    return os.path.join(
        renderOutputFolder,
        f"{seq}_{rendered_resolutions[seq][0]}x{rendered_resolutions[seq][1]}_qp{qp}_{frames}frames_8bit_yuv420.yuv",
    )


def getRenderLogFilePath(seq, qp):
    return os.path.join(renderOutputFolder, f"{seq}_qp{qp}.log")


def getRawYuvPath(seq):
    return os.path.join(
        inputFolder,
        f"{seq}_{resolutions[seq][0]}x{resolutions[seq][1]}_300frames_8bit_yuv420.yuv",
    )


def run_task(seq, qp):
    print(f"Starting task for {seq} with QP {qp}...")
    start_time = time.time()  # Record start time

    # ========================= start =========================

    width, height = resolutions[seq]

    # 1. vvc codec
    vvc_codec(
        encoder,
        getRawYuvPath(seq),
        getCodecYuvPath(seq, qp),
        os.path.join(configFolder, "vtm_RA.cfg"),
        width,
        height,
        frames,
        qp,
        getCodecLogFilePath(seq, qp),
    )

    # 2. ffmpeg yuv2img
    image_pattern = os.path.join(getCodecImageFolderPath(seq, qp), "Image%03d.png")
    yuv2img(
        ffmpeg,
        width,
        height,
        getCodecYuvPath(seq, qp),
        image_pattern,
        getCodecLogFilePath(seq, qp),
    )

    # 3. rlc render
    frame_pattern = os.path.join(getRenderImageFolderPath(seq, qp), "frame#%03d")
    rlc_cfg_path = os.path.join(configFolder, seq, "param.cfg")
    calib_path = os.path.join(configFolder, seq, "calib.xml")

    rlc_render(
        rlc,
        rlc_cfg_path,
        image_pattern,
        frame_pattern,
        calib_path,
        0,
        frames,
        5,
        getRenderLogFilePath(seq, qp),
    )

    # 4. render result, img2yuv
    rendered_image_pattern = os.path.join(frame_pattern, "image_013.png")
    img2yuv(
        ffmpeg,
        0,
        frames,
        rendered_image_pattern,
        getRenderYuvPath(seq, qp),
        getRenderLogFilePath(seq, qp),
    )

    # ========================= end =========================

    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    print(f"Task for {seq} with QP {qp} completed in {duration:.2f} seconds.")


# max_workers = 24  # Set the maximum number of concurrent processes

with ProcessPoolExecutor(max_workers=24) as executor:
    futures = []
    for seq in seqs:
        for qp in qps[seq]:
            futures.append(executor.submit(run_task, seq, qp))

    for future in as_completed(futures):
        try:
            future.result()  # This will raise any exception that occurred in the process
        except Exception as e:
            print(f"An error occurred: {e}")
