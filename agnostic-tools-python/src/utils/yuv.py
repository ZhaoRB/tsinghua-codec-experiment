import numpy as np


def read_yuv420(filename, width, height, frames):
    # YUV420 格式的字节数
    frame_size = width * height * 3 // 2  # Y + U + V
    # 读取文件
    with open(filename, "rb") as f:
        yuv_data = f.read(frame_size * frames)

    # 计算 Y, U, V 通道的开始和结束索引
    y_size = width * height
    uv_size = y_size // 4  # U 和 V 分量每个的大小

    # 初始化返回的数组
    y_data = np.zeros((height, width, frames), dtype=np.uint8)
    u_data = np.zeros((height // 2, width // 2, frames), dtype=np.uint8)
    v_data = np.zeros((height // 2, width // 2, frames), dtype=np.uint8)

    # 读取每一帧数据
    for frame_idx in range(frames):
        offset = frame_idx * frame_size
        # Y 通道，读取完整的像素
        y_data[:, :, frame_idx] = np.frombuffer(
            yuv_data[offset : offset + y_size], dtype=np.uint8
        ).reshape((height, width))
        # U 通道，读取下采样后的数据
        u_data[:, :, frame_idx] = np.frombuffer(
            yuv_data[offset + y_size : offset + y_size + uv_size], dtype=np.uint8
        ).reshape((height // 2, width // 2))
        # V 通道，读取下采样后的数据
        v_data[:, :, frame_idx] = np.frombuffer(
            yuv_data[offset + y_size + uv_size : offset + frame_size], dtype=np.uint8
        ).reshape((height // 2, width // 2))

    # 重采样 U, V 通道
    u_resized = np.zeros((height, width, frames), dtype=np.uint8)
    v_resized = np.zeros((height, width, frames), dtype=np.uint8)

    for i in range(height // 2):
        for j in range(width // 2):
            u_resized[i * 2 : i * 2 + 2, j * 2 : j * 2 + 2, :] = u_data[i, j, :]
            v_resized[i * 2 : i * 2 + 2, j * 2 : j * 2 + 2, :] = v_data[i, j, :]

    # 合并 Y, U, V 数据
    yuv = np.stack(
        [y_data, u_resized, v_resized], axis=-1
    )  # shape = (height, width, 3, frames)
    yuv = np.moveaxis(yuv, -1, 0)  # shape = (frames, height, width, 3)

    print(yuv.shape)

    return yuv


def write_yuv420(filename, yuv, width, height):
    # 获取帧数
    frames = yuv.shape[3]

    print(frames)

    # 提取 Y、U、V 通道
    y_data = yuv[0, :, :, :]
    u_data = yuv[1, :, :, :]
    v_data = yuv[2, :, :, :]

    # 将 YUV 分量保存为 YUV420 格式
    frame_size = width * height * 3 // 2  # 每帧的字节数

    # 打开文件进行写入
    with open(filename, "wb") as f:
        for frame_idx in range(frames):
            # 计算每一帧的 Y、U、V 数据
            y_frame = y_data[:, :, frame_idx].reshape((height, width))
            u_frame = u_data[::2, ::2, frame_idx].reshape(
                (height // 2, width // 2)
            )  # 下采样 U 通道
            v_frame = v_data[::2, ::2, frame_idx].reshape(
                (height // 2, width // 2)
            )  # 下采样 V 通道

            # 将 Y、U、V 数据按 YUV420 格式写入文件
            f.write(y_frame.tobytes())
            f.write(u_frame.tobytes())
            f.write(v_frame.tobytes())


if __name__ == "__main__":
    input_path = "/home/zrb/project/tsinghua-codec-experiment/agnostic-tools-python/data/raw/Boys_3976x2956_300frames_8bit_yuv420.yuv"
    yuvArray = read_yuv420(input_path, 3976, 2956, 10)
    output_path = "/home/zrb/project/tsinghua-codec-experiment/agnostic-tools-python/data/raw/Boys_output.yuv"
    write_yuv420(output_path, yuvArray, 3976, 2956)
