import os

from initialize import *
from tasks.format_convert import img2yuv

# summaryLogFile = os.path.join(summaryOutputFolder, "summary.log")

seqs = ["HandTools", "Motherboard2", "MiniGarden2"]
qps = {
    "HandTools": [41],
    "Motherboard2": [39],
    "MiniGarden2": [40],
}

# /workspace/zrb/data/mepg149-cmcc-0122/render/MiniGarden2_qp40/

def run_summary(seq):
    for qp in qps[seq]:
        print(f"Start summary for {seq} QP {qp}...")

        for i in range(viewNum * viewNum):
            index = i + 1
            curImagePattern = f"image_{index:03}.png"

            curQpYuv = getSummaryTempQpYuv(seq, qp, index)

            img2yuv(
                ffmpeg,
                startFrame,
                frames,
                os.path.join(getRenderFramePattern(seq, qp), curImagePattern),
                curQpYuv,
            )


if __name__ == "__main__":
    for seq in seqs:
        run_summary(seq)