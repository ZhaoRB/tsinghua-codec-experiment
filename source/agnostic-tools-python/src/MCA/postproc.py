import numpy as np
from common.lvc_config import SeqInfo


# 合并背景图像（行和列压缩的背景部分）
def mergeBackground(
    row_squeezed_image: np.ndarray,
    col_squeezed_image: np.ndarray,
    seq_info: SeqInfo,
) -> np.ndarray:
    patch_size = int(round(seq_info.diameter / np.sqrt(2)))
    if patch_size % 2 == 1:  # Ensure patch_size is even
        patch_size += 1

    background_image = np.zeros(
        (seq_info.height, seq_info.width, 3), dtype=col_squeezed_image.dtype
    )

    # First, combine the column-wise squeezed image
    src_lx = 0
    dst_lx = 0
    for col in range(seq_info.colNum):
        src_rx = int(seq_info.allCenterPoints[0, col, 0] - patch_size // 2)
        dst_rx = dst_lx + src_rx - src_lx
        background_image[:, src_lx:src_rx] = col_squeezed_image[:, dst_lx:dst_rx]
        dst_lx = dst_rx
        src_lx = src_rx + patch_size
    background_image[:, src_lx:] = col_squeezed_image[:, dst_lx:]

    # Now combine the row-wise squeezed image
    dst_lx = 0
    for col in range(seq_info.colNum):
        src_lx = int(seq_info.allCenterPoints[0, col, 0] - patch_size // 2)
        src_rx = src_lx + patch_size
        dst_rx = dst_lx + patch_size

        src_ty = 0
        dst_ty = 0
        for row in range(seq_info.rowNum):
            src_by = int(seq_info.allCenterPoints[row, col, 1] - patch_size // 2)
            dst_by = dst_ty + src_by - src_ty
            background_image[src_ty:src_by, src_lx:src_rx] = row_squeezed_image[
                dst_ty:dst_by, dst_lx:dst_rx
            ]

            src_ty = src_by + patch_size
            dst_ty = dst_by

        background_image[src_ty:, src_lx:src_rx] = row_squeezed_image[
            dst_ty:, dst_lx:dst_rx
        ]

        dst_lx = dst_rx

    return background_image


# 将 main_image 和合并后的背景图像重新拼接
def mergeImages(
    main_image: np.ndarray, background_image: np.ndarray, seq_info: SeqInfo
) -> np.ndarray:
    patch_size = int(round(seq_info.diameter / np.sqrt(2)))
    if patch_size % 2 == 1:
        patch_size += 1

    merged_image = np.zeros(
        (seq_info.height, seq_info.width, 3), dtype=main_image.dtype
    )

    for i in range(seq_info.rowNum):
        for j in range(seq_info.colNum):
            cur_point = seq_info.allCenterPoints[i, j]

            top_left_x = int(cur_point[0] - patch_size // 2)
            top_left_y = int(cur_point[1] - patch_size // 2)
            bottom_right_x = int(cur_point[0] + patch_size // 2)
            bottom_right_y = int(cur_point[1] + patch_size // 2)

            new_top_left_x = j * patch_size
            new_top_left_y = i * patch_size

            merged_image[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = (
                main_image[
                    new_top_left_y : new_top_left_y + patch_size,
                    new_top_left_x : new_top_left_x + patch_size,
                ]
            )

    merged_image += background_image

    return merged_image
