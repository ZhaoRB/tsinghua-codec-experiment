import cv2
from common.parser import parse_config
from init import *
from MCA.postproc import *

if __name__ == "__main__":
    for seq in seqs:
        task_info, seq_info = parse_config(getConfigPath(seq))

        main_image = cv2.imread(getPreMainPath(seq))
        background_row_squeezed_image = cv2.imread(getPreBackRowPath(seq))
        background_col_squeezed_image = cv2.imread(getPreBackColPath(seq))

        merged_background_image = mergeBackground(
            background_row_squeezed_image, background_col_squeezed_image, seq_info
        )
        merged_image = mergeImages(main_image, merged_background_image, seq_info)

        cv2.imwrite(getPostPath(seq), merged_image)
