import logging
import subprocess


def img2yuv(ffmpeg, startFrame, frames, input_images, output_yuv, logFilePath):
    # Configure logging to write to logfilePath
    logging.basicConfig(
        filename=logFilePath,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Log the start of the task
    logging.info(
        f"[LVC TEST]: img2yuv started with input images: {input_images} and output: {output_yuv}"
    )

    try:
        with open(logFilePath, "a") as logFile:
            subprocess.run(
                [
                    ffmpeg,
                    "-start_number",
                    str(startFrame),
                    "-i",
                    input_images,
                    "-vf",
                    "format=yuv420p",
                    "-frames:v",
                    str(frames),
                    output_yuv,
                    "-y",
                ],
                stdout=logFile,
                stderr=subprocess.STDOUT,
            )

        # Log the successful completion of the task
        logging.info(
            f"[LVC TEST]: img2yuv completed successfully with output: {output_yuv}"
        )

    except subprocess.CalledProcessError as e:
        # Log the error if subprocess fails
        logging.error(
            f"[LVC TEST]: img2yuv failed for input: {input_images}. Error: {str(e)}"
        )


def yuv2img(ffmpeg, width, height, input_yuv, output_images, logFilePath):
    # Configure logging to write to logfilePath
    logging.basicConfig(
        filename=logFilePath,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Log the start of the task
    logging.info(
        f"[LVC TEST]: yuv2img started with input: {input_yuv} and output images: {output_images}"
    )

    try:
        with open(logFilePath, "a") as logFile:
            subprocess.run(
                [
                    ffmpeg,
                    "-s",
                    f"{width}x{height}",
                    "-pix_fmt",
                    "yuv420p",
                    "-i",
                    input_yuv,
                    output_images,
                    "-y",
                ],
                stdout=logFile,
                stderr=subprocess.STDOUT,
            )

        # Log the successful completion of the task
        logging.info(
            f"[LVC TEST]: yuv2img completed successfully with output images: {output_images}"
        )

    except subprocess.CalledProcessError as e:
        # Log the error if subprocess fails
        logging.error(
            f"[LVC TEST]: yuv2img failed for input: {input_yuv}. Error: {str(e)}"
        )
