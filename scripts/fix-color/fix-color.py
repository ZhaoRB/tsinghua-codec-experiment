import math
import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance


# feat: 调整颜色平衡 RGB
def adjustColorBalance(img, rRatio, gRatio, bRatio):
    # 转换为 numpy 数组
    image_array = np.array(img)

    # 分离 RGB 通道
    red, green, blue = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]

    # 应用比例调整
    red = np.clip(red * rRatio, 0, 255)
    green = np.clip(green * gRatio, 0, 255)
    blue = np.clip(blue * bRatio, 0, 255)

    # 合并调整后的通道
    adjusted_image_array = np.stack([red, green, blue], axis=2).astype("uint8")

    # 转换回图像
    adjusted_image = Image.fromarray(adjusted_image_array)

    return adjusted_image


# feat: 调整亮度
def adjustBrightness(img, ratio):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(ratio)  # 增加亮度，参数>1增加亮度，<1降低亮度


# feat: 调整部分像素的亮度（提亮暗部，亮部不变）
def adjustBrightnessSmooth(img, min_ratio, max_ratio, min_threshold, max_threshold):
    # Convert image to RGB if it is not already
    img = img.convert("RGB")
    pixels = img.load()

    # Loop over each pixel and adjust brightness
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            # Convert RGB to grayscale to get brightness
            brightness = 0.299 * r + 0.587 * g + 0.114 * b

            if brightness < min_threshold:
                ratio = max_ratio
            elif brightness > max_threshold:
                ratio = min_ratio
            else:
                # Linearly interpolate the ratio based on brightness
                ratio = min_ratio + (max_ratio - min_ratio) * (
                    max_threshold - brightness
                ) / (max_threshold - min_threshold)

            # Adjust pixel values by the interpolated ratio
            r = min(int(r * ratio), 255)
            g = min(int(g * ratio), 255)
            b = min(int(b * ratio), 255)

            # Update pixel with new values
            pixels[i, j] = (r, g, b)

    return img


# feat: 按照对数函数的形式调整亮度
def adjustBrightnessLog(img, min_ratio, max_ratio, min_threshold, max_threshold):
    # Convert image to RGB if it is not already
    img = img.convert("RGB")
    pixels = img.load()

    # Loop over each pixel and adjust brightness using a logarithmic function
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            # Convert RGB to grayscale to get brightness
            brightness = 0.299 * r + 0.587 * g + 0.114 * b

            # Apply a logarithmic function to the brightness
            log_brightness = math.log(brightness + 1)  # Adding 1 to avoid log(0)

            # Calculate the ratio based on the logarithmic brightness
            if log_brightness < min_threshold:
                ratio = max_ratio
            elif log_brightness > max_threshold:
                ratio = min_ratio
            else:
                # Linearly interpolate the ratio based on the logarithmic brightness
                ratio = min_ratio + (max_ratio - min_ratio) * (
                    log_brightness - min_threshold
                ) / (max_threshold - min_threshold)

            # Adjust pixel values by the interpolated ratio
            r = min(int(r * ratio), 255)
            g = min(int(g * ratio), 255)
            b = min(int(b * ratio), 255)

            # Update pixel with new values
            pixels[i, j] = (r, g, b)

    return img


# feat: 调整对比度
def adjustContrast(img, ratio):
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(ratio)  # 增加对比度，参数>1增加对比度，<1降低对比度


# feat: 调整颜色饱和度
def adjustColor(img, ratio):
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(ratio)  # 增加对比度，参数>1增加对比度，<1降低对比度


# feat: 画图
def drawImage(images):
    num_images = len(images)
    fig, axes = plt.subplots(1, num_images, figsize=(6 * num_images, 6))

    for ax, (img, title) in zip(axes, images):
        ax.imshow(img)
        ax.set_title(title)
        ax.axis("off")

    plt.show()


def drawBrightnessGraph(img):
    # 将图片转换为numpy数组
    img_array = np.array(img)

    # 计算灰度值
    gray_array = (
        0.299 * img_array[..., 0]
        + 0.587 * img_array[..., 1]
        + 0.114 * img_array[..., 2]
    )

    # 绘制灰度图
    plt.imshow(gray_array, cmap="gray")
    plt.colorbar()  # 显示颜色条
    plt.title("Brightness Map")
    plt.show()


if __name__ == "__main__":
    input_folder = (
        "/mnt/d/Tsinghua/Codec-Data/lvc-test-sequences-images/TSPC/Boys/images"
    )
    output_folder = "/mnt/d/Tsinghua/Projects/tsinghua-codec-experiment/data/fix-color/fix-color-raw/Boys"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(300):  # 遍历 image000.bmp 到 image299.bmp
        image_name = f"Image{i:03d}.bmp"
        input_path = os.path.join(input_folder, image_name)

        if os.path.exists(input_path):
            raw_image = Image.open(input_path)

            # 进行图像调整
            image = adjustColorBalance(raw_image, 1.04, 0.96, 0.96)
            image = adjustBrightnessSmooth(image, 1.1, 1.4, 50, 200)
            image = adjustColor(image, 1.1)

            # 保存修改后的图像
            output_path = os.path.join(output_folder, image_name)
            image.save(output_path)
            print(f"Saved: {output_path}")
        else:
            print(f"File not found: {input_path}")
