import cv2


names = ["Motherboard"]

for name in names:
    input_path = f"/data/ZRB/sequences/{name}/img_001.bmp"
    output_path = f"/home/zrb/project/tsinghua-codec-experiment/data/sample/{name}.png"
    img = cv2.imread(input_path)
    cv2.imwrite(output_path, img)

