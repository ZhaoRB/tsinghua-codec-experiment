import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

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


def run_task(seq, qp):
    pattern = 5 if seq in ["NagoyaFujita", "NagoyaOrigami"] else 6

    inputFolder = "/home/data/mpeg148-anchor/render"
    input_pattern = os.path.join(inputFolder, seq, "frame#%03d", "image_%03d.png")

    outputFolder = "/home/data/mpeg148-anchor/subjective"
    os.makedirs(outputFolder, exist_ok=True)

    outputPath = os.path.join(outputFolder, f"{seq}_qp{qp}_1920x1080_8bit_yuv420p")

    subprocess.run(
        [
            "python",
            "./tasks/pose_trace_generation.py",
            input_pattern,
            outputPath,
            "-p",
            pattern,
            "-pad",
            "1920x1080",
        ]
    )


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
