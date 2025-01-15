# Python script to sort the yuv files by their names

# 读取文件内容
with open('./hash_results.txt', 'r') as file:
    lines = file.readlines()

# 将每一行的内容按空格分隔，提取文件名部分进行排序
sorted_lines = sorted(lines, key=lambda line: line.split()[0])

# 将排序后的结果写回文件
with open('./hash_results.txt', 'w') as file:
    file.writelines(sorted_lines)

print("文件已按文件名排序并写回。")
