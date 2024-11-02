import os

# =================== parameters =================
# The run scripts are executed in multiple processes, max_workers set the maximum number of processes
max_workers = 24

frames = 300
startFrame = 0

viewNum = 5
centerImageToConvert = "image_013.png"

paramFileName = "param.cfg"
calibFileName = "calib.xml"

encoder = "./executable/EncoderAppStatic"
ffmpeg = "./executable/ffmpeg"
# rlc = "./executable/RLC-BoxFuji"
# rlc = "./executable/RLC-TSPC"

inputFolder = "/workspace/zrb/data/MPEG148-Sequences"
outputFolder = "/workspace/zrb/data/mpeg148-anchor"
configFolder = "./config"

# inputFolder = "/home/data/mpeg148-sequences"
# outputFolder = "/home/data/mpeg148-anchor"

# outputFolder = "/data/back-up/1031-render-backup"

seqs = [
    # "Boys",
    "MiniGarden2",
    "HandTools",
    "Motherboard2",
    "Matryoshka",
]
rlc = "./executable/RLC-TSPC"
# seqs = [
#     "NagoyaFujita",
# ]
# rlc = "./executable/RLC-BoxFuji"
# seqs = ["NagoyaOrigami"]
# rlc = "./executable/RLC-Origami"

qps = {
    "Boys": [36, 40, 44, 48, 52],
    "HandTools": [42, 46, 50, 54],
    "MiniGarden2": [34, 38, 42, 46, 50, 54],
    "Motherboard2": [38, 42, 46, 50, 54],
    "Matryoshka": [40, 44, 48, 52, 56, 60],
    "NagoyaFujita": [32, 36, 40, 44, 48, 52],
    "NagoyaOrigami": [32, 36, 40, 44],
}
qps = {
    "Boys": [36, 40, 44, 48, 52],
    "HandTools": [50, 54],
    "MiniGarden2": [50, 54],
    "Motherboard2": [50, 54],
    "Matryoshka": [52, 56, 60],
    "NagoyaFujita": [32, 36, 40, 44, 48, 52],
    "NagoyaOrigami": [32, 36, 40, 44],
}

# ===================== you only need to adjust the parameters above =================


# resolutions
resolutions = {
    "Boys": [3976, 2956],
    "HandTools": [4036, 3064],
    "Motherboard2": [4036, 3064],
    "MiniGarden2": [4036, 3064],
    "Matryoshka": [4040, 3064],
    "NagoyaFujita": [2048, 2048],
    "NagoyaOrigami": [2048, 2048],
    "Boxer-IrishMan-Gladiator": [3840, 2160],
}

rendered_resolutions = {
    "Boys": [1348, 980],
    "HandTools": [1370, 1004],
    "Motherboard2": [1370, 1004],
    "MiniGarden2": [1370, 1004],
    "Matryoshka": [1370, 1004],
    "NagoyaFujita": [740, 732],
    "NagoyaOrigami": [706, 692],
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


# codec output
def getCodecYuvPath(seq, qp):
    return os.path.join(
        codecOutputFolder,
        f"{seq}_{resolutions[seq][0]}x{resolutions[seq][1]}_qp{qp}_{frames}frames_8bit_yuv420.yuv",
    )


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
renderSubjectiveOutputFolder = "../../mpeg148-anchor/render-subjective"
os.makedirs(renderSubjectiveOutputFolder, exist_ok=True)


def getSubjectiveInputPattern(seq, qp):
    return os.path.join(
        renderOutputFolder, f"{seq}_qp{qp}", framePattern, renderedImagePattern
    )


def getSubjectiveRenderYuvPath(seq, qp):
    return os.path.join(
        renderSubjectiveOutputFolder,
        f"{seq}_qp{qp}_1920x1080_{frames}frames_8bit_yuv420.yuv",
    )


# =================== render subjective base =================
renderSubjectiveBaseOutputFolder = "../../mpeg148-anchor/render-subjective-base"
os.makedirs(renderSubjectiveBaseOutputFolder, exist_ok=True)


def getSubjectiveBaseInputPattern(seq):
    return os.path.join(renderBaseOutputFolder, seq, framePattern, renderedImagePattern)


def getSubjectiveBaseRenderYuvPath(seq):
    return os.path.join(
        renderBaseOutputFolder,
        f"{seq}_1920x1080_{frames}frames_8bit_yuv420.yuv",
    )


# =================== summary =================
csvFileName = os.path.join(outputFolder, "summary.csv")

all_seqs = [
    "Boys",
    "HandTools",
    "MiniGarden2",
    "Motherboard2",
    "Matryoshka",
    "NagoyaFujita",
    "NagoyaOrigami",
]

all_qps = {
    "Boys": [36, 40, 44, 48, 52],
    "HandTools": [34, 38, 42, 46, 50, 54],
    "MiniGarden2": [34, 38, 42, 46, 50, 54],
    "Motherboard2": [34, 38, 42, 46, 50, 54],
    "Matryoshka": [40, 44, 48, 52, 56, 60],
    "NagoyaFujita": [32, 36, 40, 44, 48, 52],
    "NagoyaOrigami": [24, 28, 32, 36, 40, 44, 48, 52],
    # "Boxer-IrishMan-Gladiator": [32, 36, 40, 44, 48, 52],
}
