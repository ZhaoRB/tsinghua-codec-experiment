import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from tasks.codec import vvc_codec
from tasks.format_convert import img2yuv, yuv2img
from tasks.render import rlc_render

# parameters
inputFolder = "/home/zrb/data/mpeg148-tspc-seqs"
outputFolder = "/home/zrb/data/codec-output-30frames"
configFolder = "/home/zrb/project/tsinghua-codec-experiment/experiment/config"

frameToBeEncoded = 30
qps = [48, 46, 44, 42, 40, 38, 36, 34, 32, 30]
qps = [48]
seqs = ["Boys", "HandTools", "NewMotherboard", "MiniGarden"]
seqs = ["Boys"]

max_workers = 16  # Set the maximum number of concurrent processes


def run_task(seq, qp):
    print(f"Starting task for {seq} with QP {qp}...")
    start_time = time.time()  # Record start time

    log_file = os.path.join(outputFolder, f"{seq}_qp{qp}.log")

    width = 3976 if seq == "Boys" else 4036
    height = 2956 if seq == "Boys" else 3064

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
    output_yuv2img = os.path.join(outputFolder, f"codec-{seq}_qp{qp}", "Image%03d.png")
    os.makedirs(output_yuv2img, exist_ok=True)

    yuv2img(ffmpeg, width, height, output_yuv, output_yuv2img, log_file)

    # 3. rlc render
    output_render = os.path.join(outputFolder, f"render-{seq}_qp{qp}", "frame#%03d")
    os.makedirs(output_render, exist_ok=True)

    rlc = "/home/zrb/project/tsinghua-codec-experiment/experiment/executable/RLC40"
    rlc_cfg_path = os.path.join(outputFolder, seq, "param.cfg")
    calib_path = os.path.join(outputFolder, seq, "calib.xml")

    rlc_render(
        rlc,
        rlc_cfg_path,
        output_yuv2img,
        output_render,
        calib_path,
        0,
        frameToBeEncoded,
        5,
    )

    # 4. render result, img2yuv
    rendered_width = 1348
    rendered_height = 980 if seq == "Boys" else 1004

    input_img2yuv = os.path.join(output_render, "image_013.png")
    output_render_yuv = os.path.join(
        outputFolder,
        f"render-{seq}_qp{qp}_{rendered_width}x{rendered_height}_{frameToBeEncoded}frames.yuv",
    )
    img2yuv(ffmpeg, 0, frameToBeEncoded, input_img2yuv, output_render_yuv, log_file)

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
