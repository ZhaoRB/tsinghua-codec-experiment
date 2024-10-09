from config import Config

def run_one_task(
    task_name: str,
    config: Config,
    seq_name: str,
    former_name: str,
    vtm_type: str,
    qp: int,
) -> str:
    task = config.task
    path = config.path

    commands = {
        "img2yuv": [
            "ffmpeg",
            "-start_number",
            task.start_frame,
            "-i",
            f"{path.input_folder}/{seq_name}/{task.img_pattern}",
            "-vf",
            "format=yuv420p",
            "-frames:v",
            task.frames,
            f"{path.output_folder}/{seq_name}_",
            "-y",  # overwrite without confirmation
        ],
        "yuv2img": [],
        "vvc_codec": [],
        "rlc_render": [],
        "mca_pre": [],
        "mca_post": [],
    }
