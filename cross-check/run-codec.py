import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from tasks.codec import vvc_codec
from tasks.format_convert import yuv2img

# parameters
inputFolder = "/home/data/mpeg148-sequences"
outputFolder = "/home/data/codec-300frames-mpeg148-sequences"
configFolder = "./config"

frameToBeEncoded = 300

# seqs = ["Matryoshka", "NagoyaFujita", "NagoyaOrigami"]
# seqs = ["Boys"]
seqs = ["HandTools", "MiniGarden", "NewMotherboard", "Boys"]
qps = {
    "Boys": [36, 40, 44, 48],
    "HandTools": [54, 50, 46, 42, 38],
    "NewMotherboard": [54, 50, 46, 42, 38],
    "MiniGarden": [54, 50, 46, 42, 38],
    # "Matryoshka": [36, 40, 44, 48, 52, 56, 60],
    # "NagoyaFujita": [24, 28, 32, 36, 40, 44, 48],
    # "NagoyaOrigami": [24, 28, 32, 36, 40, 44, 48],
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

max_workers = 16  # Set the maximum number of concurrent processes

encoder = "./executable/EncoderAppStatic"
ffmpeg = "./executable/ffmpeg"
rlc = "./executable/RLC40-1025"


def getYuvFileName(seq, w, h, frames=300, qp=0):
    filename = (
        f"{seq}_{w}x{h}_{frames}frames_8bit_yuv420.yuv"
        if qp == 0
        else f"codec-{seq}_{w}x{h}_qp{qp}_{frames}frames_8bit_yuv420.yuv"
    )
    return filename


def run_task(seq, qp):
    print(f"Starting task for {seq} with QP {qp}...")
    start_time = time.time()  # Record start time

    os.makedirs(os.path.join(outputFolder, "log"), exist_ok=True)
    log_file = os.path.join(outputFolder, "log", f"{seq}_qp{qp}.log")

    width = resolutions[seq][0]
    height = resolutions[seq][1]

    # 1. vvc codec
    input_yuv = os.path.join(inputFolder, getYuvFileName(seq, width, height))

    codec_output_folder = os.path.join(outputFolder, "codec")
    os.makedirs(codec_output_folder, exist_ok=True)

    output_bitstream = os.path.join(
        codec_output_folder, f"codec-{seq}_qp{qp}_bitstream"
    )
    output_yuv = os.path.join(
        codec_output_folder, getYuvFileName(seq, width, height, frameToBeEncoded, qp)
    )

    vvc_codec(
        encoder,
        input_yuv,
        output_bitstream,
        output_yuv,
        os.path.join(configFolder, "vtm_RA.cfg"),
        width,
        height,
        frameToBeEncoded,
        qp,
        log_file,
    )

    # 2. ffmpeg yuv2img
    output_yuv2img_folder = os.path.join(codec_output_folder, f"codec-{seq}_qp{qp}")
    output_yuv2img = os.path.join(
        codec_output_folder, f"codec-{seq}_qp{qp}", "Image%03d.png"
    )
    os.makedirs(output_yuv2img_folder, exist_ok=True)

    yuv2img(ffmpeg, width, height, output_yuv, output_yuv2img, log_file)

    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    print(f"Task for {seq} with QP {qp} completed in {duration:.2f} seconds.")


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
