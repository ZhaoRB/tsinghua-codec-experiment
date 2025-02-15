import math
import numpy as np
import yuvio

def calc_array_psnr(lhs: np.ndarray, rhs: np.ndarray) -> float:
    mse = np.mean((lhs.astype(np.int16) - rhs.astype(np.int16)) ** 2)
    if mse == 0:
        return np.inf
    return 20 * math.log10(255.0 / math.sqrt(mse))


def calc_yuv_psnr(lhs, rhs, width: int, height: int) -> np.ndarray:
    lhs_reader = yuvio.get_reader(lhs, width, height, "yuv420p")
    rhs_reader = yuvio.get_reader(rhs, width, height, "yuv420p")
    if len(lhs_reader) != len(rhs_reader):
        raise RuntimeError(f"Frame count not equal! lhs={lhs} rhs={rhs}")

    psnr_acc = np.zeros(3)
    count = 0

    for lhs_frame, rhs_frame in zip(lhs_reader, rhs_reader, strict=True):
        psnr_acc[0] += calc_array_psnr(lhs_frame.y, rhs_frame.y)
        psnr_acc[1] += calc_array_psnr(lhs_frame.u, rhs_frame.u)
        psnr_acc[2] += calc_array_psnr(lhs_frame.v, rhs_frame.v)
        count += 1

    psnr = psnr_acc / count

    return psnr

if __name__ == '__main__':
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
    
    psnr = calc_yuv_psnr(yuv_file1, yuv_file2, width, height)
    print(psnr)