import os

from codec import vvc_codec

base_path = "/home/zrb/project/tsinghua-codec-experiment/agnostic-tools-python/data"
main_name = "Boys_3250x2050_main"
back_row_name = "Boys_3250x906_back_row"
back_col_name = "Boys_726x2956_back_col"

main_input = os.path.join(base_path, "preproc", f"{main_name}.yuv")
back_row_input = os.path.join(base_path, "preproc", f"{back_row_name}.yuv")
back_col_input = os.path.join(base_path, "preproc", f"{back_col_name}.yuv")

main_output = os.path.join(base_path, "pre-codec", f"{main_name}.yuv")
back_row_output = os.path.join(base_path, "pre-codec", f"{back_row_name}.yuv")
back_col_output = os.path.join(base_path, "pre-codec", f"{back_col_name}.yuv")

main_log = os.path.join(base_path, "pre-codec", f"{main_name}.log")
back_row_log = os.path.join(base_path, "pre-codec", f"{back_row_name}.log")
back_col_log = os.path.join(base_path, "pre-codec", f"{back_col_name}.log")

encoder = "./executable/EncoderAppStatic"
config = "./config/vtm_RA.cfg"
qp1 = 40
qp2 = 48

vvc_codec(encoder, main_input, main_output, config, 3250, 2050, 300, qp1, main_log)
vvc_codec(
    encoder, back_row_input, back_row_output, config, 3250, 906, 300, qp2, back_row_log
)
vvc_codec(
    encoder, back_col_input, back_col_output, config, 726, 2956, 300, qp2, back_col_log
)
