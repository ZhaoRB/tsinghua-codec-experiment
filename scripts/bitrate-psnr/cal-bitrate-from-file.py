import os

def calculate_file_size(file_path):
    # 获取文件大小（单位：字节）
    file_size = os.path.getsize(file_path)
    
    # 计算结果
    result = (file_size * 8) / 10 / 1000
    
    return result

# 输入文件路径
file_path = '/workspace/zrb/data/mpeg148-anchor/codec-bitstream/Boys_qp28_bitstream'  # 请替换为实际的文件路径

filename = ["HandTools_qp41.bin", "MiniGarden2_qp40.bin", "Motherboard2_qp39.bin"]
file_folder = '/workspace/zrb/data/tsinghua-codec-experiment/scripts/cmcc-new-qp-bin'

for fn in filename:
    file_path = os.path.join(file_folder, fn)
    res = calculate_file_size(file_path)

    print(f"{fn}: {res} kbps")
