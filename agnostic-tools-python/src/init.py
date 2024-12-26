import os

basePath = "/Users/riverzhao/Project/Codec/0_lvc_codec/lvc-codec-agnostic-tool/agnostic-tools-python/data"

seqs = ["Boys2", "MiniGarden2"]

def getConfigPath(seq):
    return os.path.join(basePath, f"../../config/{seq}/{seq}_LVC.cfg")


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
