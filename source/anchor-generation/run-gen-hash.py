import hashlib
import os


def calculate_md5(file_path):
    """计算文件的MD5值"""
    print(f"start calculate md5 hash of {file_path}...")
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
    print(f"finish calculate md5 hash of {file_path}...")


def search_yuv_files(directory):
    """递归搜索指定文件夹中的所有yuv文件"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".yuv"):
                yield os.path.join(root, file)


def write_hashes_to_file(directory, output_file):
    """将yuv文件的路径和MD5值写入到输出文件"""
    with open(output_file, "w") as f_out:
        for yuv_file in search_yuv_files(directory):
            file_name = os.path.basename(yuv_file)
            md5_hash = calculate_md5(yuv_file)
            f_out.write(f"{file_name}\t{md5_hash}\n")


if __name__ == "__main__":
    # 设定要搜索的文件夹路径和输出结果的文件路径
    directory_to_search = "/workspace/zrb/data/mpeg148-anchor/codec/"
    output_file = "./hash_results.txt"

    # 计算并写入MD5哈希值
    write_hashes_to_file(directory_to_search, output_file)

    print(f"Hash values of YUV files have been written to {output_file}")
