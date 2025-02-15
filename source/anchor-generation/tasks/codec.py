import logging
import subprocess


def vvc_codec(
    Encoder,
    input_yuv,
    output_yuv,
    cfgFile,
    perSeqCfg,
    # width,
    # height,
    frames,
    qp,
    logfilePath,
    output_bitstream,
):
    # Configure logging to write to logfilePath
    logging.basicConfig(
        filename=logfilePath,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Log the start of the task
    logging.info(
        f"[LVC TEST]: VVC encoding started for {input_yuv} with QP {qp}. Output will be saved to {output_yuv}\n"
    )

    try:
        with open(logfilePath, "w") as logfile:
            subprocess.run(
                [
                    Encoder,
                    "-c",
                    cfgFile,
                    "-c",
                    perSeqCfg,
                    # "-wdt",
                    # str(width),
                    # "-hgt",
                    # str(height),
                    # "-fr",
                    # "30",  # Frame rate
                    # "--InputBitDepth=8",
                    # "--OutputBitDepth=8",
                    f"--FramesToBeEncoded={frames}",
                    # "--Level=6.2",
                    # "--ConformanceMode=1",
                    f"--QP={qp}",
                    "-i",
                    input_yuv,
                    "-b",
                    output_bitstream,  # Bitstream output file name
                    "-o",
                    output_yuv,  # Reconstructed YUV output file name
                ],
                stdout=logfile,
                stderr=subprocess.STDOUT,
            )

        # Log the successful completion of the task
        logging.info(
            f"[LVC TEST]: VVC encoding completed successfully for {input_yuv} with QP {qp}\n\n"
        )

    except subprocess.CalledProcessError as e:
        # Log the error if subprocess fails
        logging.error(
            f"[LVC TEST]: VVC encoding failed for {input_yuv} with QP {qp}. Error: {str(e)}\n\n"
        )
