import os
import subprocess


def update_mca_config(app_config_path: str, config: dict, task_type: str, seqname: str, input_path: str, output_path: str):
    app_add_config = {}

    app_add_config["start_frame"] = f"{config["task"]["start_frame"]}"
    app_add_config["end_frame"] = f"{config["task"]["start_frame"] + config["task"]["frames"]}"
    
    image_pattern = config["task"]["image_pattern"]
    app_add_config["RawImage_Path"] = f"{input_path}/{image_pattern}"
    app_add_config["Output_Path"] = f"{output_path}/{image_pattern}"

    calib_file_name = task_type.split("_")[0]
    app_add_config["Calibration_xml"] = f"./config/{seqname}/{calib_file_name}.xml"

    if task_type in ("mca20_pre", "mca20_post"):
        app_add_config["supInfo_path"] = ""

    if task_type in ("mca_pre", "mca_post"):
        app_add_config["crop_ratio"] = config["mca"]["crop_ratio"]

    with open(app_config_path, "a") as app_config_file:
        app_config_file.write("\n")
        for k, v in app_add_config.items():
            app_config_file.write(f"{k} {v}\n")


def mca(config: dict, mca_task_type: str, filename: str):
    seqname = filename.split("_")[0]
    cfg_path = f"./config/{seqname}/{mca_task_type}.cfg"

    input_folder = config["task"]["input_folder"]
    output_folder = config["task"]["output_folder"]
    
    input_path = f"{input_folder if mca_task_type in ("mca_pre", "mca20_pre") else output_folder}/{filename}"
    output_filename = f"{filename}_{mca_task_type}"
    output_path = f"{output_folder}/{output_filename}"
    
    os.makedirs(output_folder, mode=0o777, exist_ok=True)
    update_mca_config(cfg_path, config, mca_task_type, seqname, input_path, output_path)

    subprocess.run([config["app"][mca_task_type], cfg_path])

    return output_filename
