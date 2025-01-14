import os

# =================== parameters =================
max_workers = 48  # run-xxx.py 脚本执行的最大进程数

frames = 300  # 要处理（如codec，render）的帧数
startFrame = 0  # 起始帧

viewNum = 5  # 渲染出的视角数
centerImageToConvert = "image_013.png"  # 中心视角图片名

# executable
scriptBasePath = "/workspace/zrb/data/tsinghua-codec-experiment/anchor-generation"
encoder = os.path.join(scriptBasePath, "./executable/EncoderAppStatic")
ffmpeg = os.path.join(scriptBasePath, "./executable/ffmpeg")
rlc = os.path.join(scriptBasePath, "./executable/RLC40")

# configuration files
configFolder = os.path.join(scriptBasePath, "./config")
vvcCfgFile = os.path.join(configFolder, "encoder_randomaccess_vtm.cfg")
paramFileName = "param.cfg"
calibFileName = "calib.xml"

inputFolder = "/workspace/zrb/data/MPEG148-Sequences"  # 输入文件夹路径
outputFolder = "/workspace/zrb/data/mpeg148-anchor"  # 输出文件夹路径
os.makedirs(outputFolder, exist_ok=True)

seqs = [
    "Boys",
    "HandTools",
    "MiniGarden2",
    "Motherboard2",
    "Matryoshka",
]

qps = {
    "Boys2": [28, 32, 36, 40, 44, 48],
    "HandTools": [34, 38, 42, 46, 50, 54],
    "MiniGarden2": [34, 38, 42, 46, 50, 54],
    "Motherboard2": [30, 34, 38, 42, 46, 50],
    "Origami": [28, 32, 36, 40, 44, 48],
    "Matryoshka": [40, 44, 48, 52],
    "Fujita2": [36, 40, 44, 48],
}

# ===================== you only need to adjust the parameters above =================

all_seqs = [
    "Boys2",
    "HandTools",
    "MiniGarden2",
    "Motherboard2",
    "Origami",
    "Matryoshka",
    "Fujita2",
]

all_qps = {
    "Boys2": [28, 32, 36, 40, 44, 48],
    "HandTools": [34, 38, 42, 46, 50, 54],
    "MiniGarden2": [34, 38, 42, 46, 50, 54],
    "Motherboard2": [30, 34, 38, 42, 46, 50],
    "Origami": [28, 32, 36, 40, 44, 48],
    # Matryoshka & Fujita only for objective test
    "Matryoshka": [40, 44, 48, 52],
    "Fujita2": [36, 40, 44, 48],
}


resolutions = {
    "Boys": [3976, 2956],
    "HandTools": [4036, 3064],
    "Motherboard2": [4036, 3064],
    "MiniGarden2": [4036, 3064],
    "Matryoshka": [4040, 3064],
    "Fujita2": [2048, 2048],
    "Origami": [2048, 2048],
    "Boxer-IrishMan-Gladiator": [3840, 2160],
    "TempleBoatGiantR32": [6464, 4852],
}

rendered_resolutions = {
    "Boys": [1098, 800],
    "HandTools": [1116, 820],
    "Motherboard2": [1116, 820],
    "MiniGarden2": [1116, 820],
    "Matryoshka": [1116, 820],
    "Fujita2": [740, 732],
    "Origami": [706, 692],
    "Boxer-IrishMan-Gladiator": [1338, 746],
}

# =================== set file names and make dirs =================
imagePattern = "Image%03d.png"
framePattern = "Frame#%03d"
renderedImagePattern = "image_%03d.png"


# =================== raw image & yuv =================
def getRawYuvPath(seq):
    return os.path.join(
        inputFolder,
        f"{seq}_{resolutions[seq][0]}x{resolutions[seq][1]}_300frames_8bit_yuv420.yuv",
    )


def getRawImagePattern(seq):
    return os.path.join(inputFolder, seq, imagePattern)


# =================== codec =================
codecOutputFolder = os.path.join(outputFolder, "codec")
os.makedirs(codecOutputFolder, exist_ok=True)

codecBitstreamFolder = os.path.join(outputFolder, "codec-bitstream")
os.makedirs(codecBitstreamFolder, exist_ok=True)


# per sequence config
def getCodecPerSeqCfg(seq):
    return os.path.join(configFolder, seq, f"./{seq}.cfg")


# codec output
def getCodecYuvPath(seq, qp):
    return os.path.join(
        codecOutputFolder,
        f"{seq}_{resolutions[seq][0]}x{resolutions[seq][1]}_qp{qp}_{frames}frames_8bit_yuv420.yuv",
    )


def getBitstreamPath(seq, qp):
    return os.path.join(codecBitstreamFolder, f"{seq}_qp{qp}_bitstream")


# yuv2img after codec
def getCodecImagePattern(seq, qp):
    filepath = os.path.join(codecOutputFolder, f"{seq}_qp{qp}")
    os.makedirs(filepath, exist_ok=True)
    return os.path.join(filepath, imagePattern)


# create the file if it doesn't exist or clear its content if it does
def getCodecLogFilePath(seq, qp):
    path = os.path.join(codecOutputFolder, f"{seq}_qp{qp}.log")
    open(path, "w").close()
    return path


# =================== render =================
renderOutputFolder = os.path.join(outputFolder, "render")
os.makedirs(renderOutputFolder, exist_ok=True)


def getRenderConfigPath(seq):
    paramPath = os.path.join(configFolder, seq, paramFileName)
    calibPath = os.path.join(configFolder, seq, calibFileName)
    return paramPath, calibPath


# render output
def getRenderFramePattern(seq, qp):
    filepath = os.path.join(renderOutputFolder, f"{seq}_qp{qp}")
    os.makedirs(filepath, exist_ok=True)
    return os.path.join(filepath, framePattern)


# convert rendered output images to yuv
def getRenderYuvPath(seq, qp):
    return os.path.join(
        renderOutputFolder,
        f"{seq}_{rendered_resolutions[seq][0]}x{rendered_resolutions[seq][1]}_qp{qp}_{frames}frames_8bit_yuv420.yuv",
    )


def getRenderLogFilePath(seq, qp):
    path = os.path.join(renderOutputFolder, f"{seq}_qp{qp}.log")
    open(path, "w").close()
    return path


# =================== render base =================
renderBaseOutputFolder = os.path.join(outputFolder, "render-base")
os.makedirs(renderBaseOutputFolder, exist_ok=True)


def getBaseRenderFramePattern(seq):
    filepath = os.path.join(renderBaseOutputFolder, seq)
    os.makedirs(filepath, exist_ok=True)
    return os.path.join(filepath, framePattern)


def getBaseRenderYuvPath(seq):
    return os.path.join(
        renderBaseOutputFolder,
        f"{seq}_{rendered_resolutions[seq][0]}x{rendered_resolutions[seq][1]}_{frames}frames_8bit_yuv420.yuv",
    )


def getBaseRenderLogFilePath(seq):
    path = os.path.join(renderBaseOutputFolder, f"{seq}.log")
    open(path, "w").close()
    return path


# =================== render subjective =================
renderSubjectiveOutputFolder = os.path.join(outputFolder, "./render-subjective")
os.makedirs(renderSubjectiveOutputFolder, exist_ok=True)


def getSubjectiveInputPattern(seq, qp):
    return os.path.join(
        renderOutputFolder, f"{seq}_qp{qp}", framePattern, renderedImagePattern
    )


def getSubjectiveRenderYuvPath(seq, qp):
    return os.path.join(
        renderSubjectiveOutputFolder,
        f"{seq}_qp{qp}_1920x1080_{frames}frames_8bit_yuv420p.yuv",
    )


# =================== render subjective base =================
renderSubjectiveBaseOutputFolder = os.path.join(
    outputFolder, "./render-subjective-base"
)
os.makedirs(renderSubjectiveBaseOutputFolder, exist_ok=True)


def getSubjectiveBaseInputPattern(seq):
    return os.path.join(renderBaseOutputFolder, seq, framePattern, renderedImagePattern)


def getSubjectiveBaseRenderYuvPath(seq):
    return os.path.join(
        renderSubjectiveBaseOutputFolder,
        f"{seq}_1920x1080_{frames}frames_8bit_yuv420p.yuv",
    )


# =================== summary =================
summaryOutputFolder = os.path.join(outputFolder, "summary")
os.makedirs(summaryOutputFolder, exist_ok=True)

csvFileNameAllSeqs = os.path.join(summaryOutputFolder, "all_summary.csv")

tempYuvFolder = os.path.join(summaryOutputFolder, "temp_yuv")
os.makedirs(tempYuvFolder, exist_ok=True)


def getSummaryTempBaseYuv(seq, index):
    return os.path.join(tempYuvFolder, f"{seq}_{index}_base.yuv")


def getSummaryTempQpYuv(seq, qp, index):
    return os.path.join(tempYuvFolder, f"{seq}_{index}_{qp}.yuv")


def getSeqCsvFileName(seq):
    return os.path.join(summaryOutputFolder, f"{seq}_summary.csv")
