import os
import hashlib

# 目标目录路径
root_directory  = r'./'

# 输出日志文件路径
output_log = r'md5.log'

# 打开输出文件
with open(output_log, 'w', newline='') as log_file:
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.yuv'):  # 检查文件是否为YUV文件
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_directory)  # 计算相对路径
                
                # 打开并读取YUV文件内容
                with open(file_path, 'rb') as yuv_file:
                    md5_hash = hashlib.md5(yuv_file.read()).hexdigest()
                
                # 写入日志文件
                log_file.write(f'{relative_path}\t{md5_hash}\n')


