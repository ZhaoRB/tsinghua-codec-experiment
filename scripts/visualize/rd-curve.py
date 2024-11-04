import csv
import os

import matplotlib.pyplot as plt

input_folder = "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment/data/find-qp/csv"
output_folder = "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment/data/find-qp/figure"
# sequence_names = ["fujita", "origami", "motherboard"]
sequence_names = ["origami"]

qps_to_plot = [26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]
qps_to_plot = [32, 36, 40, 44]
qps_to_plot = [28, 32, 36, 40]
# qps_to_plot = [36, 40, 44, 48]


def qpsToString(qpsArr):
    return "_".join(map(str, qpsArr))


for seq_name in sequence_names:
    input_path = os.path.join(input_folder, f"{seq_name}.csv")
    output_path_png = os.path.join(
        output_folder, f"{seq_name}_{qpsToString(qps_to_plot)}.png"
    )
    # output_path_svg = os.path.join(output_folder, f"{seq_name}.svg")

    bitrates = []
    mvpsnr_y_values = []

    with open(input_path, "r") as f:
        csv_data = csv.reader(f)
        # print(csv_data, "\n", type(csv_data))
        header = next(csv_data)  # Skip header

        for row in csv_data:
            qp = int(row[1])
            if qp in qps_to_plot:
                bitrate = float(row[2])
                mvpsnr_y = float(row[6])

                bitrates.append(bitrate)
                mvpsnr_y_values.append(mvpsnr_y)

    if bitrates and mvpsnr_y_values:
        plt.figure()
        plt.plot(bitrates, mvpsnr_y_values, marker="o")
        plt.xlabel("Total Bitrate (kbps)")
        plt.ylabel("MVPSNR-Y (dB)")
        plt.title(f"{seq_name}")
        plt.grid(True)
        plt.savefig(output_path_png)
        # plt.savefig(output_path_svg)
        plt.close()
