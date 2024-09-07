"""
    Project:  Restore
    Author:  PengH
    Date:  2024/9/7 12:25
"""

import os
import math
from PIL import Image, ImageEnhance

# 损坏透镜的左上角坐标
row = 2605
col = 3790

# 损坏透镜的中心坐标(x轴向左，y轴向下)
center_x = 3827
center_y = 2641


# 计算像素点到损坏透镜中心的距离
# 判断该像素点是否在损坏区域内
def dis(x, y):
    return math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)


# 曝光后对透镜图像边缘进行模糊处理，平滑图像
def obscure(img):
    pixels = img.load()

    for i in range(0, 75):
        for j in range(0, 75):
            d = dis(col + j, row + i)
            if 25 <= d <= 35:
                pixel_up = pixels[col + j - 1, row + i]
                pixel_left = pixels[col + j, row + i - 1]
                pixel_right = pixels[col + j, row + i + 1]
                pixel_down = pixels[col + j + 1, row + i]

                r = int((pixel_up[0] + pixel_left[0] + pixel_right[0] + pixel_down[0]) / 4)
                g = int((pixel_up[1] + pixel_left[1] + pixel_right[1] + pixel_down[1]) / 4)
                b = int((pixel_up[2] + pixel_left[2] + pixel_right[2] + pixel_down[2]) / 4)

                img.putpixel((col + j, row + i), (r, g, b))


# 对单张图片进行修复
def single_img(input_path, output_path):
    img = Image.open(input_path)

    enhancer = ImageEnhance.Brightness(img)
    brightness_image = enhancer.enhance(3)

    pixels = img.load()

    for i in range(0, 75):
        for j in range(0, 75):
            d = dis(col + j, row + i)
            if d <= 35:
                img.putpixel((col + j, row + i), brightness_image.load()[col + j, row + i])

    for i in range(0, 75):
        for j in range(0, 75):
            d = dis(col + j, row + i)
            if 30 <= d <= 35:
                pixel = pixels[col + j, row + i]
                r = int(pixel[0] * 0.5 * 35 / d)
                g = int(pixel[1] * 0.5 * 35 / d)
                b = int(pixel[2] * 0.5 * 35 / d)

                img.putpixel((col + j, row + i), (r, g, b))

    # 连续平滑两次
    obscure(img)
    obscure(img)

    img.save(output_path)


# 遍历文件夹，批量操作
def scanImage(_input_dir, _output_dir):
    files = os.listdir(_input_dir)

    for file in files:
        input_file_path = os.path.join(_input_dir, file)
        output_file_path = os.path.join(_output_dir, file)

        if file == '.DS_Store':
            continue

        if os.path.isfile(input_file_path):
            single_img(input_file_path, output_file_path)

        elif os.path.isdir(input_file_path):
            scanImage(input_file_path, output_file_path)


if __name__ == '__main__':
    input_dir = input('Enter input directory name: ')
    output_dir = input('Enter output directory name: ')
    scanImage(input_dir, output_dir)
