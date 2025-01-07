from common.parser import parse_config
from init_yuv import *
from MCA.postproc_yuv import *
from utils.yuv import *

if __name__ == "__main__":
    for seq in seqs:
        task_info, seq_info = parse_config(getConfigPath(seq))

        main_yuv = read_yuv420(getPreCodecMainPath("Boys", 3250, 2050), 3250, 2050, frames)
        row_squeezed_yuv = read_yuv420(
            getPreCodecBackRowPath("Boys", 3250, 906), 3250, 906, frames
        )
        col_squeezed_yuv = read_yuv420(
            getPreCodecBackColPath("Boys", 726, 2956), 726, 2956, frames
        )

        merged_yuv = merge_yuv(
            main_yuv, row_squeezed_yuv, col_squeezed_yuv, seq_info, frames
        )

        write_yuv420(
            getPostPath(seq),
            merged_yuv,
            resolutions[seq][0],
            resolutions[seq][1],
        )
