import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from tasks.codec import vvc_codec
from tasks.format_convert import yuv2img

# parameters
inputFolder = "/home/data/mpeg148-tspc-seqs"
outputFolder = "/home/data/1021-tspc-multiQP-codec-render"
configFolder = "/home/zrb/project/tsinghua-codec-experiment/experiment/config"

frameToBeEncoded = 30

seqs = ["Matryoshka", "NagoyaFujita", "NagoyaOrigami"]
qps = {
    "Matryoshka": [36, 40, 44, 48, 52, 56, 60],
    "NagoyaFujita": [24, 28, 32, 36, 40, 44, 48],
    "NagoyaOrigami": [24, 28, 32, 36, 40, 44, 48],
}
resolutions= {
    "Matryoshka": [4040, 3064],
    "NagoyaFujita": [2048, 2048],
    "NagoyaOrigami": [2048, 2048],
}

max_workers = 24  # Set the maximum number of concurrent processes

def run_task(seq, qp):
    print(f"Starting task for {seq} with QP {qp}...")
    start_time = time.time()  # Record start time

    log_file = os.path.join(outputFolder, f"{seq}_qp{qp}.log")

    width = resolutions[seq][0]
    height = resolutions[seq][1]

    # 1. vvc codec
    input_yuv = os.path.join(
        inputFolder, f"{seq}_{width}x{height}_300frames_8bit_yuv420.yuv"
    )
    output_bitstream = os.path.join(outputFolder, f"codec-{seq}_qp{qp}_bitstream")
    output_yuv = os.path.join(
        outputFolder,
        f"codec-{seq}_{width}x{height}_qp{qp}_{frameToBeEncoded}frames_8bit_yuv420p.yuv",
    )

    encoder = "/home/zrb/project/tsinghua-codec-experiment/experiment/executable/EncoderAppStatic"

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
    ffmpeg = "ffmpeg"
    output_yuv2img_folder = os.path.join(outputFolder, f"codec-{seq}_qp{qp}")
    output_yuv2img = os.path.join(outputFolder, f"codec-{seq}_qp{qp}", "Image%03d.png")
    os.makedirs(output_yuv2img_folder, exist_ok=True)

    yuv2img(ffmpeg, width, height, output_yuv, output_yuv2img, log_file)

    end_time = time.time()  # Record end time
    duration = end_time - start_time  # Calculate duration
    print(f"Task for {seq} with QP {qp} completed in {duration:.2f} seconds.")


with ProcessPoolExecutor(max_workers=max_workers) as executor:
    futures = []
    for seq in seqs:
        for qp in qps:
            futures.append(executor.submit(run_task, seq, qp))

    for future in as_completed(futures):
        try:
            future.result()  # This will raise any exception that occurred in the process
        except Exception as e:
            print(f"An error occurred: {e}")


# for seq in seqs:
#     for qp in qps:
#         run_task(seq, qp)
