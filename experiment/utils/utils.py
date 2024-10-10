import os


def update_config(configFilePath: str, config: dict, type: str, filename: str, seqname: str):
    app_config = {}

    with open(configFilePath, "r") as app_config_file:
        for line in app_config_file:
            k, v = line.strip().split()
            app_config[k] = v

    app_config["Calibration_xml"] = f"./config/calib.xml"
    app_config["RawImage_Path"] = f""
    app_config["Output_Path"] = f""
    app_config["start_frame"] = f"{config["task"]["start_frame"]}"
    app_config["end_frame"] = f"{config["task"]["start_frame"] + config["task"]["frames"]}"

    if type == "mca20":
        app_config["supInfo_path"] = ""
        app_config["supInfo_path"] = ""
    if type == "mca":
        app_config["crop_ratio"] = ""
    if type == "rlc40":
        app_config["viewNum"] = config[""]

    with open(configFilePath, "w") as app_config_file:
        for k, v in app_config.items():
            app_config_file.write(f"{k} {v}\n")


# def get_paths(seqname: str, config: dict):
#     output = config["task"]["output_folder"]
    
#     raw_res = config['raw_res'][seqname]
#     mca_res = config['mca_res'][seqname]
#     mca20_res = config['mca20_res'][seqname]

#     paths = {
#         "mca_pre": f"{output}/mca_pre_{seqname}",
#         "mca_pre_yuv": f"{output}/{seqname}_wMCA_{mca_res[0]}x{mca_res[1]}_{config["task"]["frames"]}frames_8bit.yuv",
#         "mca20_pre": f"{output}/mca20_pre_{seqname}",
#         "mca20_pre_yuv": f"{output}/{seqname}_wMCA20_{mca_res[0]}x{mca_res[1]}_{config["task"]["frames"]}frames_8bit.yuv",
#     }
# # "mca_pre_codec": f"{output}/mca_pre_{seqname}",
# #         "mca_pre_codec_yuv": f"{output}/{seqname}_wMCA_{mca_res[0]}x{mca_res[1]}_{config["task"]["frames"]}frames_8bit.yuv",
    
#     qps = ['base'] + config["qps"][seqname]
#     for qp in qps:



# def make_dir(paths: list[str]):
#     for p in paths:
#         if not os.path.exists(p):
#             os.makedirs(p)
