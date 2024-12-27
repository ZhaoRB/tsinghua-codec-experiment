from common.parser import parse_config
from init_yuv import *
from MCA.preproc_yuv import *
from utils.yuv import *

if __name__ == "__main__":
    for seq in seqs:
        task_info, seq_info = parse_config(getConfigPath(seq))
        raw_yuv = read_yuv420(
            getRawYuvPath(seq), seq_info.width, seq_info.height, frames
        )

        (
            main_yuv,
            main_height,
            main_width,
            row_squeezed_yuv,
            row_squeezed_width,
            row_squeezed_height,
            col_squeezed_yuv,
            col_squeezed_width,
            col_squeezed_height,
        ) = mca_yuv(raw_yuv, seq_info, frames)

        write_yuv420(
            getPreMainPath(seq, main_width, main_height),
            main_yuv,
            main_width,
            main_height,
        )
        write_yuv420(
            getPreBackRowPath(seq, row_squeezed_width, row_squeezed_height),
            row_squeezed_yuv,
            row_squeezed_width,
            row_squeezed_height,
        )
        write_yuv420(
            getPreBackColPath(seq, col_squeezed_width, col_squeezed_height),
            col_squeezed_yuv,
            col_squeezed_width,
            col_squeezed_height,
        )
