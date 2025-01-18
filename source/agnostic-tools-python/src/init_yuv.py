import os

basePath = "/home/zrb/project/tsinghua-codec-experiment/agnostic-tools-python/data"
seqs = ["Boys"]
frames = 300

resolutions = {"Boys": [3976, 2956]}


def getConfigPath(seq):
    return os.path.join(basePath, f"../config/{seq}_LVC.cfg")


def getRawYuvPath(seq):
    return os.path.join(basePath, f"./raw/{seq}.yuv")


# =========================== pre =========================== 
def getPreMainPath(seq, w, h):
    return os.path.join(basePath, f"./preproc/{seq}_{w}x{h}_main.yuv")


def getPreBackPath(seq):
    return os.path.join(
        basePath,
        f"./preproc/{seq}_{resolutions[seq][0]}x{resolutions[seq][1]}_back.yuv",
    )


def getPreBackRowPath(seq, w, h):
    return os.path.join(
        basePath,
        f"./preproc/{seq}_{w}x{h}_back_row.yuv",
    )


def getPreBackColPath(seq, w, h):
    return os.path.join(basePath, f"./preproc/{seq}_{w}x{h}_back_col.yuv")


# =========================== post ===========================
def getPostPath(seq):
    return os.path.join(
        basePath,
        f"./postproc/{seq}_{resolutions[seq][0]}x{resolutions[seq][1]}_merged.yuv",
    )

# =========================== pre codec =========================== 
def getPreCodecMainPath(seq, w, h):
    return os.path.join(basePath, f"./pre-codec/{seq}_{w}x{h}_main.yuv")


def getPreCodecBackRowPath(seq, w, h):
    return os.path.join(
        basePath,
        f"./pre-codec/{seq}_{w}x{h}_back_row.yuv",
    )


def getPreCodecBackColPath(seq, w, h):
    return os.path.join(basePath, f"./pre-codec/{seq}_{w}x{h}_back_col.yuv")