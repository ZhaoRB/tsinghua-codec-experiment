import re


def if_codec_finish(logFile):
    target_line = "Total Frames |   Bitrate     Y-PSNR    U-PSNR    V-PSNR    YUV-PSNR"
    with open(logFile, "r") as file:
        for line in file:
            if target_line in line:
                return True
    return False


def extract_codec_info(logFilePath):

    # 读取log文件内容
    with open(logFilePath, "r") as file:
        log_content = file.read()

    # 定义匹配的正则表达式模式
    pattern = r"(\d+)\s+[a-zA-Z]+\s+([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)"

    # 搜索匹配的内容
    match = re.search(pattern, log_content)

    if match:
        # total_frames = int(match.group(1))
        bitrate = float(match.group(2))
        y_psnr = float(match.group(3))
        u_psnr = float(match.group(4))
        v_psnr = float(match.group(5))
        # yuv_psnr = float(match.group(6))
        return [bitrate, y_psnr, u_psnr, v_psnr]

    else:
        print("No matching data found.")
        return []
