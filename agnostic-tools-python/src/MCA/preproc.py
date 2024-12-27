import numpy as np
from common.lvc_config import SeqInfo


def cropAndRealign(
    image: np.ndarray, seq_info: SeqInfo
) -> tuple[np.ndarray, np.ndarray]:
    patch_size = int(round(seq_info.diameter / np.sqrt(2)))
    if patch_size % 2 == 1:
        patch_size += 1

    width, height = patch_size * seq_info.colNum, patch_size * seq_info.rowNum
    new_image = np.zeros((height, width, 3), dtype=image.dtype)
    masked_image = image.copy()

    for i in range(seq_info.rowNum):
        for j in range(seq_info.colNum):
            # Get the center point for the current patch
            cur_point = seq_info.allCenterPoints[i, j]

            # Calculate the top-left and bottom-right corners of the square patch
            top_left_x = int(cur_point[0] - patch_size // 2)
            top_left_y = int(cur_point[1] - patch_size // 2)
            bottom_right_x = int(cur_point[0] + patch_size // 2)
            bottom_right_y = int(cur_point[1] + patch_size // 2)

            # Extract the patch from the original image
            patch = image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

            # Compute where to place this patch in the new image
            new_top_left_x = j * patch_size
            new_top_left_y = i * patch_size

            # Place the patch into the corresponding location in the new image
            new_image[
                new_top_left_y : new_top_left_y + patch.shape[0],
                new_top_left_x : new_top_left_x + patch.shape[1],
            ] = patch

            masked_image[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = 0

    return new_image, masked_image


def backgroundCropAndRealign(background_image: np.ndarray, seq_info: SeqInfo):
    patch_size = int(round(seq_info.diameter / np.sqrt(2)))
    if patch_size % 2 == 1:  # Ensure patch_size is even
        patch_size += 1

    row_squeezed_image_width = patch_size * seq_info.colNum
    row_squeezed_image_height = seq_info.height - patch_size * seq_info.rowNum
    col_squeezed_image_width = seq_info.width - row_squeezed_image_width
    col_squeezed_image_height = seq_info.height

    row_squeezed_image = np.zeros(
        (row_squeezed_image_height, row_squeezed_image_width, 3),
        dtype=background_image.dtype,
    )
    col_squeezed_image = np.zeros(
        (col_squeezed_image_height, col_squeezed_image_width, 3),
        dtype=background_image.dtype,
    )

    # squeeze cols
    src_lx = 0
    dst_lx = 0
    for col in range(seq_info.colNum):
        src_rx = int(seq_info.allCenterPoints[0, col, 0] - patch_size // 2)
        dst_rx = dst_lx + src_rx - src_lx
        col_squeezed_image[:, dst_lx:dst_rx] = background_image[:, src_lx:src_rx]
        dst_lx = dst_rx
        src_lx = src_rx + patch_size
    col_squeezed_image[:, dst_lx:] = background_image[:, src_lx:]

    # squeeze rows
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
            row_squeezed_image[dst_ty:dst_by, dst_lx:dst_rx] = background_image[
                src_ty:src_by, src_lx:src_rx
            ]

            src_ty = src_by + patch_size
            dst_ty = dst_by

        row_squeezed_image[dst_ty:, dst_lx:dst_rx] = background_image[
            src_ty:, src_lx:src_rx
        ]

        dst_lx = dst_rx

    return row_squeezed_image, col_squeezed_image
