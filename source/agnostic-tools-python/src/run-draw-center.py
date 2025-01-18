import cv2
from common.parser import parse_config
from utils.draw_center import draw_centers

if __name__ == "__main__":
    seq_name = "MiniGarden2"
    input_file = f"../data/raw-image/{seq_name}.png"
    center_file = f"../data/analysis/calib_center_{seq_name}.png"
    config_file = f"../../config/{seq_name}/{seq_name}_LVC.cfg"

    task_info, seq_info = parse_config(config_file)
    raw_image = cv2.imread(input_file)

    draw_centers(raw_image, seq_info.allCenterPoints, seq_info.diameter, center_file)
