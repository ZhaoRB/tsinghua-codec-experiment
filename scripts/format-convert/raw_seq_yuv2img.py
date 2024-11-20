import os
import subprocess

resolutions = {
    "Boys": [3976, 2956],
    "HandTools": [4036, 3064],
    "Motherboard2": [4036, 3064],
    "MiniGarden2": [4036, 3064],
    "Matryoshka": [4040, 3064],
    "NagoyaFujita": [2048, 2048],
    "NagoyaOrigami": [2048, 2048],
    "Boxer-IrishMan-Gladiator": [3840, 2160],
    "TempleBoatGiantR32": [6464, 4852],
}

seqs = [
    "Boys",
    "HandTools",
    "MiniGarden2",
    "Motherboard2",
    "NagoyaOrigami",
    "Matryoshka",
    "NagoyaFujita",
]

inputFolder = "/workspace/zrb/data/new-mpeg148-sequences/"


def yuv2img(seq):
    os.makedirs(os.path.join(inputFolder, seq), exist_ok=True)

    subprocess.run(
        [
            "/workspace/zrb/data/tsinghua-codec-experiment/cross-check/executable/ffmpeg",
            "-s",
            f"{resolutions[seq][0]}x{resolutions[seq][1]}",
            "-pix_fmt",
            "yuv420p",
            "-i",
            os.path.join(
                inputFolder,
                f"{seq}_{resolutions[seq][0]}x{resolutions[seq][1]}_300frames_8bit_yuv420.yuv",
            ),
            "-start_number",
            "0",
            os.path.join(inputFolder, seq, "Image%03d.png"),
            "-y",
        ],
    )

if __name__ == "__main__":
    for seq in seqs:
        yuv2img(seq)