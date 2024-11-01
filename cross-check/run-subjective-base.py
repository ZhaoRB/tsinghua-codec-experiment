import os
import subprocess

from initialize import *


def run_task(seq):
    raytrixSequences = ["NagoyaFujita", "NagoyaOrigami"]
    pattern = 5 if seq in raytrixSequences else 6

    subprocess.run(
        [
            "python",
            "./tasks/pose_trace_generation.py",
            getSubjectiveBaseInputPattern(seq),
            os.path.join(
                renderSubjectiveBaseOutputFolder, f"{seq}_1920x1080_8bit_yuv420p.yuv"
            ),
            "-p",
            f"{pattern}",
            "-pad",
            "1920x1080",
        ]
    )


if __name__ == "__main__":
    for seq in seqs:
        run_task(seq)
