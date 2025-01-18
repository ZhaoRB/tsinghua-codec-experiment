import cv2
from common.parser import parse_config
from init import *
from MCA.preproc import *

if __name__ == "__main__":
    for seq in seqs:
        task_info, seq_info = parse_config(getConfigPath(seq))
        raw_image = cv2.imread(getRawImagePath(seq))

        main_image, background_image = cropAndRealign(raw_image, seq_info)
        print(f"cropped image shape is {main_image.shape}")

        background_row_squeezed_image, background_col_squeezed_image = (
            backgroundCropAndRealign(background_image, seq_info)
        )

        cv2.imwrite(getPreMainPath(seq), main_image)
        cv2.imwrite(getPreBackPath(seq), background_image)
        cv2.imwrite(getPreBackRowPath(seq), background_row_squeezed_image)
        cv2.imwrite(getPreBackColPath(seq), background_col_squeezed_image)
