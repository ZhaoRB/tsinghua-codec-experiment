import numpy as np
from common.lvc_config import SeqInfo
from MCA.postproc import *


def merge_yuv(
    main_yuv: np.ndarray,
    row_squeeze_yuv: np.ndarray,
    col_squeeze_yuv: np.ndarray,
    seq_info: SeqInfo,
    frames,
):
    yuv_data = np.zeros((frames, seq_info.height, seq_info.width, 3), dtype=np.uint8)

    for i in range(frames):
        background_img = mergeBackground(
            row_squeeze_yuv[i, :, :, :], col_squeeze_yuv[i, :, :, :], seq_info
        )
        yuv_data[i, :, :, :] = mergeImages(
            main_yuv[i, :, :, :], background_img, seq_info
        )

    return yuv_data
