import os
import re

# 配置文件夹路径
input_folder = '/home/data/lvc-raw-sequences'
output_folder = '/home/data/lvc-raw-sequences-30frames'

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 获取input文件夹中的所有YUV420文件
yuv_files = [f for f in os.listdir(input_folder) if f.endswith('.yuv')]

# 设置正则表达式来从文件名中提取width和height
file_name_pattern = re.compile(r'(\d+)x(\d+)')

# 读取YUV420文件并提取前30帧
for yuv_file in yuv_files:
    match = file_name_pattern.search(yuv_file)
    if not match:
        print(f"跳过文件 {yuv_file}，无法从文件名中提取宽度和高度")
        continue
    
    # 从文件名中提取width和height
    width = int(match.group(1))
    height = int(match.group(2))
    
    # 计算YUV420格式的一帧大小
    frame_size = width * height + (width // 2) * (height // 2) * 2
    
    # 输入和输出文件路径
    input_path = os.path.join(input_folder, yuv_file)
    output_file_name = yuv_file.replace('300frames', '30frames')
    output_path = os.path.join(output_folder, output_file_name)
    
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        for i in range(30):
            # 读取一帧数据
            frame_data = f_in.read(frame_size)
            if not frame_data:
                break
            # 写入输出文件
            f_out.write(frame_data)

    print(f'处理完文件: {yuv_file}, 输出到: {output_path}')

print("所有文件处理完毕")
