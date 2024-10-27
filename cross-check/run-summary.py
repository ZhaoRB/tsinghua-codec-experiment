import csv
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

from utils.extract import extract_codec_info
from utils.psnr import compute_psnr_for_yuv

baseFolder = "/home/data/find-qp"
# sequences = ["HandTools", "NewMotherboard", "MiniGarden"]

sequences = ["Matryoshka", "NagoyaFujita", "NagoyaOrigami"]
# qps = {
#     "Boys": [36, 40, 44, 48],
#     "HandTools": [30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54],
#     "NewMotherboard": [30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54],
#     "MiniGarden": [30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54],
# }
qps = {
    "Matryoshka": [36, 40, 44, 48, 52, 56, 60],
    "NagoyaFujita": [24, 28, 32, 36, 40, 44, 48],
    "NagoyaOrigami": [24, 28, 32, 36, 40, 44, 48],
}

rendered_resolutions = {
    "Matryoshka": [1370, 1004],
    "NagoyaFujita": [888, 904],
    "NagoyaOrigami": [888, 904],
}


def run_task(seq):
    width = rendered_resolutions[seq][0]
    height = rendered_resolutions[seq][1]

    frames = 30
    csvFileName = os.path.join(baseFolder, "summary", f"{seq}_summary.csv")

    # Open the CSV file for writing
    with open(csvFileName, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Sequence Name",
                "QP",
                "Bitrate",
                # "LLPSNR_Y",
                # "LLPSNR_U",
                # "LLPSNR_V",
                "MVPSNR_Y",
                "MVPSNR_U",
                "MVPSNR_V",
            ]
        )

        for qp in qps[seq]:
            # logfile = os.path.join(baseFolder, "log", f"{seq}_qp{qp}.log")
            # bitrate, llpsnr_y, llpsnr_u, llpsnr_v = extract_codec_info(logfile)

            baseYuv = os.path.join(
                baseFolder,
                "render-base",
                f"render-{seq}_base_{width}x{height}_{frames}frames.yuv",
            )
            curQpYuv = os.path.join(
                baseFolder,
                "render",
                f"render-{seq}_qp{qp}_{width}x{height}_{frames}frames.yuv",
            )
            mvpsnr_y, mvpsnr_u, mvpsnr_v = compute_psnr_for_yuv(
                baseYuv, curQpYuv, width, height
            )

            # Write data row for the current sequence and qp value
            writer.writerow(
                [
                    seq,
                    qp,
                    # bitrate,
                    # llpsnr_y,
                    # llpsnr_u,
                    # llpsnr_v,
                    mvpsnr_y,
                    mvpsnr_u,
                    mvpsnr_v,
                ]
            )


# with ProcessPoolExecutor(max_workers=16) as executor:
#     futures = []
#     for seq in sequences:
#         futures.append(executor.submit(run_task, seq))

#     for future in as_completed(futures):
#         try:
#             future.result()  # This will raise any exception that occurred in the process
#         except Exception as e:
#             print(f"An error occurred: {e}")

for seq in sequences:
    run_task(seq)
