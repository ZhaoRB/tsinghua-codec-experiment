# %%
import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance

# 打开图像
image_folder = "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment/data/fix-color"
image_name = "rendered-raw/boys_image_013.png"
raw_image = Image.open(os.path.join(image_folder, image_name))
image = raw_image


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


# %%
image = adjustColorBalance(image, 1.04, 0.96, 0.96)
image = adjustBrightness(image, 1.15)
image = adjustColor(image, 1.1)

image2 = adjustColorBalance(raw_image, 1.04, 0.96, 0.96)
image2 = adjustBrightnessSmooth(image2, 1.05, 1.3, 50, 200)
image2 = adjustColor(image2, 1.1)
drawImage(
    [
        (raw_image, "raw image"),
        (image, "adjusted image"),
        (image2, "adjusted image brighter"),
    ]
)

# %%
# 保存调整后的图像
output_name = "boys_image_fix_color.png"
image.save(os.path.join(image_folder, "fix-color-rendered-raw", output_name))
output_name = "boys_image_fix_color_brighter.png"
image2.save(os.path.join(image_folder, "fix-color-rendered-raw", output_name))
