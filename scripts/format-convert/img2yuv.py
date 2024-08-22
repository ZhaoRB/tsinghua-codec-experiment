import subprocess

# 设置输入文件夹的路径
input_pattern = "/mnt/e/ZRB/240819-4-rendered/frame#%03d/image_013.png"

# 设置输出文件路径
output_file = "/mnt/e/ZRB/new_sequence_1378x1012_350frames.yuv"

# 调用 ffmpeg 直接进行转换
subprocess.run([
    "ffmpeg",
    "-start_number", "1",
    "-i", input_pattern,
    "-frames:v", "300",
    "-pix_fmt", "yuv420p",
    output_file
])

print(f"YUV420 video has been saved to {output_file}")
