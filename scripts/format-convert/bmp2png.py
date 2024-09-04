from PIL import Image

# 打开 BMP 图像文件
img = Image.open('path_to_your_bmp_image.bmp')

# 将图像保存为 PNG 格式
img.save('output_image.png', 'PNG')