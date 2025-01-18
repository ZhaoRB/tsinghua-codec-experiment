import numpy as np
from common.lvc_config import SeqInfo
from MCA.preproc import *


def mca_yuv(yuv_data: np.ndarray, seq_info: SeqInfo, frames):
    # confirm resolutions
    img = yuv_data[0, :, :, :]
    main_img, background_img = cropAndRealign(img, seq_info)
    main_width, main_height = main_img.shape[1], main_img.shape[0]
    row_squeezed_image, col_squeezed_image = backgroundCropAndRealign(
        yuv_data[0, :, :, :], seq_info
    )
    row_squeezed_width, row_squeezed_height = (
        row_squeezed_image.shape[1],
        row_squeezed_image.shape[0],
    )
    col_squeezed_width, col_squeezed_height = (
        col_squeezed_image.shape[1],
        col_squeezed_image.shape[0],
    )

    # init yuv data
    main_yuv = np.zeros((frames, main_height, main_width, 3), dtype=np.uint8)
    row_squeezed_yuv = np.zeros(
        (frames, row_squeezed_height, row_squeezed_width, 3),
        dtype=np.uint8,
    )
    col_squeezed_yuv = np.zeros(
        (frames, col_squeezed_height, col_squeezed_width, 3), dtype=np.uint8
    )

    # crop and realign
    for i in range(frames):
        img = yuv_data[i, :, :, :]
        main_img, background_img = cropAndRealign(img, seq_info)
        main_yuv[i, :, :, :] = main_img

        row_squeezed_image, col_squeezed_image = backgroundCropAndRealign(
            background_img, seq_info
        )
        row_squeezed_yuv[i, :, :, :] = row_squeezed_image
        col_squeezed_yuv[i, :, :, :] = col_squeezed_image

    return (
        main_yuv,
        main_height,
        main_width,
        row_squeezed_yuv,
        row_squeezed_width,
        row_squeezed_height,
        col_squeezed_yuv,
        col_squeezed_width,
        col_squeezed_height,
    )
