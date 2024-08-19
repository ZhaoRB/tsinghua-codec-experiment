import subprocess

# 设置输入文件夹的路径
input_pattern = "path_to_your_frames_directory/frame%03d/image_013.png"

# 设置输出文件路径
output_file = "path_to_your_frames_directory/output.yuv"

# 调用 ffmpeg 直接进行转换
subprocess.run([
    "ffmpeg",
    "-i", input_pattern,
    "-pix_fmt", "yuv420p",
    output_file
])

print(f"YUV420 video has been saved to {output_file}")
