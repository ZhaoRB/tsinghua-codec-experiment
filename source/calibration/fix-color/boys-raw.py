# %%
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
image_folder = "/Users/riverzhao/Project/Codec/3_experiment/tsinghua-codec-experiment/data/fix-color"
input_folder = os.path.join(image_folder, "rendered-raw")
output_folder = os.path.join(image_folder, "fix-color-rendered-raw")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for i in range(300):  # 遍历 image000.bmp 到 image299.bmp
    image_name = f"image{i:03d}.bmp"
    input_path = os.path.join(input_folder, image_name)

    if os.path.exists(input_path):
        raw_image = Image.open(input_path)
        image = raw_image

        # 进行图像调整
        image = adjustColorBalance(image, 1.04, 0.96, 0.96)
        image = adjustBrightness(image, 1.15)
        image = adjustColor(image, 1.1)

        # 保存修改后的图像
        output_name = f"image{i:03d}_fix_color.png"
        output_path = os.path.join(output_folder, output_name)
        image.save(output_path)
        print(f"Saved: {output_path}")
    else:
        print(f"File not found: {input_path}")


drawImage(
    [
        (raw_image, "raw image"),
        (image, "adjusted image"),
    ]
)
