# 如何使用
1. 修改 initialize.py 中的配置
   ```python
   max_workers = 32  # run-xxx.py 脚本执行的最大进程数

   inputFolder = "/workspace/zrb/data/MPEG148-Sequences" # 输入文件夹路径
   outputFolder = "/workspace/zrb/data/mpeg148-anchor" # 输出文件夹路径

    # 序列名称
    seqs = [
        "Boys",
        "HandTools",
        "MiniGarden2",
        "Motherboard2",
        "NagoyaOrigami",
        "Matryoshka",
        "NagoyaFujita",
    ]

    # qp点
    qps = {
        "Boys": [28, 32, 36, 40, 44, 48],
        "HandTools": [34, 38, 42, 46, 50, 54],
        "MiniGarden2": [34, 38, 42, 46, 50, 54],
        "Motherboard2": [30, 34, 38, 42, 46, 50],
        "NagoyaOrigami": [28, 32, 36, 40, 44, 48],
        "Matryoshka": [40, 44, 48, 52],
        "NagoyaFujita": [36, 40, 44, 48],
    }
   ```
2. 此次 cross-check 需要测试的左右所有序列 & qp点，见 `initialize.py` 中的 `all_seqs` 和 `all_qps`
3. 运行脚本：
   - `cd cross-check`
   - `run-xxx.py`
     - `run-codec.py` 运行编码
     - `run-render.py` 运行编解码之后的序列的多视角渲染
     - `run-render-base.py` 运行原始序列的多视角渲染
     - `run-subjective.py` 编解码之后的序列的主观测试序列生成（需要先完成相应的render）
     - `run-subjective-base.py` 原始序列的主观测试序列生成（需要先完成相应的render-base）
     - `run-summary.py` 实验结果整理，生成多个summary csv文件
     - `run-visualize.py` 画 RD Curve


# input 文件夹目录 & 命名规则
1. input 文件夹：
   存放原始的图片序列 & yuv视频序列


2. output 文件夹：
   ```
    ├── codec
    ├── codec-bitstream
    ├── render
    ├── render-base
    ├── render-subjective
    ├── render-subjective-base
    ├── summary
   ```
    - codec 文件夹存放编码输出的 yuv 文件，以及 yuv 转为图片序列的文件夹，以及编码的log文件
    - codec-bitstream 存放编码输出的码流
    - render 文件夹存放**经过编解码后的序列**渲染多视角的结果
    - render-base 存放**原始序列**直接渲染多视角的结果
    - render-subjective 存放**经过编解码后的序列**转换为主观测试（pose trace）格式的结果
    - render-subjective-base 存放**原始序列**转换为主观测试（pose trace）格式的结果
    - summary 存放summary csv文件和rd-curve
