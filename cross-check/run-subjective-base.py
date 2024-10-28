import os
import subprocess

seqs = [
    "Boys",
    "MiniGarden",
    "HandTools",
    "NewMotherboard",
    "Matryoshka",
    "NagoyaFujita",
    "NagoyaOrigami",
]

raytrixSequences = ["NagoyaFujita", "NagoyaOrigami", "Boxer-IrishMan-Gladiator"]

inputFolder = "/home/data/mpeg148-anchor/render-base"
outputFolder = "/home/data/mpeg148-anchor/render-base-subjective"
os.makedirs(outputFolder, exist_ok=True)


def run_task(seq):
    pattern = 5 if seq in raytrixSequences else 6

    input_pattern = os.path.join(inputFolder, seq, "frame#%03d", "image_%03d.png")
    outputPath = os.path.join(outputFolder, f"{seq}_1920x1080_8bit_yuv420p")

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


if __name__ == "__main__":
    for seq in seqs:
        run_task(seq)
