import numpy as np


def read_yuv420(file_path, width, height):
    """
    读取 YUV420 文件并返回 Y、U、V 分量数组。
    :param file_path: YUV420 文件路径
    :param width: 视频帧的宽度
    :param height: 视频帧的高度
    :return: (Y, U, V) 分量数组
    """
    with open(file_path, "rb") as f:
        y_size = width * height
        uv_size = (width // 2) * (height // 2)

        # 读取 Y 分量
        Y = np.frombuffer(f.read(y_size), dtype=np.uint8).reshape((height, width))

        # 读取 U 分量
        U = np.frombuffer(f.read(uv_size), dtype=np.uint8).reshape(
            (height // 2, width // 2)
        )

        # 读取 V 分量
        V = np.frombuffer(f.read(uv_size), dtype=np.uint8).reshape(
            (height // 2, width // 2)
        )

    return Y, U, V


def compute_psnr(yuv_file1, yuv_file2, width, height):
    """
    分别计算 Y、U、V 分量的 PSNR
    :param yuv_file1: 第一个 YUV420 文件路径
    :param yuv_file2: 第二个 YUV420 文件路径
    :param width: 视频帧的宽度
    :param height: 视频帧的高度
    :return: 一个字典，包含 Y、U、V 分量的 PSNR 值
    """
    Y1, U1, V1 = read_yuv420(yuv_file1, width, height)
    Y2, U2, V2 = read_yuv420(yuv_file2, width, height)

    def calculate_psnr(channel1, channel2):
        mse = np.mean((channel1 - channel2) ** 2)
        if mse == 0:
            return float("inf")  # 如果没有误差，PSNR 为无穷大
        psnr = 10 * np.log10((255**2) / mse)
        return psnr

    psnr_y = calculate_psnr(Y1, Y2)
    psnr_u = calculate_psnr(U1, U2)
    psnr_v = calculate_psnr(V1, V2)

    return {"Y": psnr_y, "U": psnr_u, "V": psnr_v}


if __name__ == "__main__":
    resolutions = {
        "Boys": [3976, 2956],
        "HandTools": [4036, 3064],
        "Motherboard2": [4036, 3064],
        "MiniGarden2": [4036, 3064],
        "Matryoshka": [4040, 3064],
        "Fujita2": [2048, 2048],
        "Origami": [2048, 2048],
        "Boxer-IrishMan-Gladiator2": [3840, 2160],
        "TempleBoatGiantR32": [6464, 4852],
    }

    seqname = "Boys"
    width = resolutions[seqname][0]
    height = resolutions[seqname][1]

    yuv_file1 = f"/workspace/zrb/data/mpeg148-anchor/codec/{seqname}_{width}x{height}_qp36_300frames_8bit_yuv420.yuv"
    yuv_file2 = f"/workspace/zrb/data/lvc-raw-sequences/{seqname}2_{width}x{height}_300frames_8bit_yuv420.yuv"

    psnr_values = compute_psnr(yuv_file1, yuv_file2, width, height)
    print(f"PSNR for Y channel: {psnr_values['Y']} dB")
    print(f"PSNR for U channel: {psnr_values['U']} dB")
    print(f"PSNR for V channel: {psnr_values['V']} dB")
