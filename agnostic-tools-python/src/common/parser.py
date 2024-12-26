from common.lvc_config import *


def parse_config(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    args = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):  # Ignore comments and empty lines
            continue

        key, values = line.split(":")
        key = key.strip()
        values = values.split()
        args[key] = values

    task_info = TaskInfo(
        inputFile=args["InputFile"],
        outputFiles=args["OutputFiles"],
        framesToBeEncoded=args["FramesToBeEncoded"],
    )

    seq_info = SeqInfo(
        width=int(args["SourceWidth"][0]),
        height=int(args["SourceHeight"][0]),
        diameter=float(args["MIDiameter"][0]),
        ltop=np.array(list(map(float, args["LeftTopMICenter"]))),
        rtop=np.array(list(map(float, args["RightTopMICenter"]))),
        lbot=np.array(list(map(float, args["LeftBottomMICenter"]))),
        rbot=np.array(list(map(float, args["RightBottomMICenter"]))),
        isVertical=True if int(args["MLADirection"][0]) == 0 else False,
        rowNum=0,
        colNum=0,
        allCenterPoints=np.array([]),
    )
    seq_info.calRowAndColNum()
    seq_info.calAllCenters()
    seq_info.calibAllCenters()

    return task_info, seq_info
