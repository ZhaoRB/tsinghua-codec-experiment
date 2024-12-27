import os

basePath = "/home/zrb/project/tsinghua-codec-experiment/agnostic-tools-python/data"

seqs = ["Boys"]

def getConfigPath(seq):
    return os.path.join(basePath, f"../config/{seq}_LVC.cfg")

# ========================= image =============================
def getRawImagePath(seq):
    return os.path.join(basePath, f"./raw-image/{seq}.png")


def getPreMainPath(seq):
    return os.path.join(basePath, f"./preproc/{seq}_main.png")


def getPreBackPath(seq):
    return os.path.join(basePath, f"./preproc/{seq}_back.png")


def getPreBackRowPath(seq):
    return os.path.join(basePath, f"./preproc/{seq}_back_row.png")


def getPreBackColPath(seq):
    return os.path.join(basePath, f"./preproc/{seq}_back_col.png")


def getPostPath(seq):
    return os.path.join(basePath, f"./postproc/{seq}_merged.png")
