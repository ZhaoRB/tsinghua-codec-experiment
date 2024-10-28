import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from tasks.codec import vvc_codec
from tasks.format_convert import img2yuv, yuv2img
from tasks.render import rlc_render

# parameters
inputFolder = "/home/data/mpeg148-sequences"
outputFolder = "/home/data/find-qp"
# configFolder = "./config"
configFolder = "/home/zrb/project/tsinghua-codec-experiment/cross-check/config"

frameToBeEncoded = 30

seqs = ["Matryoshka", "NagoyaFujita", "NagoyaOrigami"]
# seqs = ["NagoyaFujita", "NagoyaOrigami"]
qps = {
    "Matryoshka": [36, 40, 44, 48, 52, 56, 60],
    "NagoyaFujita": [24, 28, 32, 36, 40, 44, 48],
    "NagoyaOrigami": [24, 28, 32, 36, 40, 44, 48],
    # "Matryoshka": [60],
    # "NagoyaFujita": [48],
    # "NagoyaOrigami": [48],
}
resolutions = {
    "Matryoshka": [4040, 3064],
    "NagoyaFujita": [2048, 2048],
    "NagoyaOrigami": [2048, 2048],
}

rendered_resolutions = {
    "Matryoshka": [1370, 1004],
    "NagoyaFujita": [888, 904],
    "NagoyaOrigami": [888, 904],
}

max_workers = 24  # Set the maximum number of concurrent processes

encoder = "./executable/EncoderAppStatic"
ffmpeg = "./executable/ffmpeg"
rlc = "./executable/RLC40"


def getYuvFileName(seq, w, h, frames=300, qp=0):
    filename = (
        f"{seq}_{w}x{h}_{frames}frames_8bit_yuv420.yuv"
        if qp == 0
        else f"codec-{seq}_{w}x{h}_qp{qp}_{frames}frames_8bit_yuv420.yuv"
    )
    return filename


def run_task(seq, qp, convertToYuv=True):
    print(f"Starting task for {seq} with QP {qp}...")
    start_time = time.time()  # Record start time

    log_file = os.path.join(outputFolder, f"{seq}_qp{qp}.log")

    width = resolutions[seq][0]
    height = resolutions[seq][1]

    codec_output_folder = os.path.join(outputFolder, "codec")
    output_yuv2img = os.path.join(
        codec_output_folder, f"codec-{seq}_qp{qp}", "Image%03d.png"
    )

    # rlc render
    render_output_folder = os.path.join(outputFolder, "render")
    output_render_folder = os.path.join(render_output_folder, f"render-{seq}_qp{qp}")
    output_render = os.path.join(
        render_output_folder, f"render-{seq}_qp{qp}", "frame#%03d"
    )
    os.makedirs(output_render_folder, exist_ok=True)

    rlc_cfg_path = os.path.join(configFolder, seq, "param.cfg")
    calib_path = os.path.join(configFolder, seq, "calib.xml")

    rlc_render(
        rlc,
        rlc_cfg_path,
        output_yuv2img,
        output_render,
        calib_path,
        0,
        frameToBeEncoded,
        5,
        log_file,
    )

    if convertToYuv:
        # img2yuv
        rendered_width = rendered_resolutions[seq][0]
        rendered_height = rendered_resolutions[seq][1]

        input_img2yuv = os.path.join(output_render, "image_013.png")
        output_render_yuv = os.path.join(
            render_output_folder,
            f"render-{seq}_qp{qp}_{rendered_width}x{rendered_height}_{frameToBeEncoded}frames.yuv",
        )
        img2yuv(ffmpeg, 0, frameToBeEncoded, input_img2yuv, output_render_yuv, log_file)

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

# for seq in seqs:
#     for qp in qps[seq]:
#         run_task(seq, qp)
