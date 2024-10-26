import logging
import subprocess


def updateConfig(
    configFile, inputImages, outputFolder, startFrame, frames, calibFile, viewNum
):
    config_data = {}

    # Read the existing config file
    with open(configFile, "r") as file:
        for line in file:
            # Ignore empty lines and comments
            if line.strip() and not line.startswith("#"):
                key, value = line.split(maxsplit=1)
                config_data[key] = value.strip()

    # Update the necessary fields
    config_data["RawImage_Path"] = inputImages
    config_data["Output_Path"] = outputFolder
    config_data["start_frame"] = str(startFrame)
    config_data["end_frame"] = str(startFrame + frames - 1)
    config_data["Calibration_xml"] = calibFile
    config_data["viewNum"] = str(viewNum)

    # Write the updated config back to the file
    with open(configFile, "w") as file:
        for key, value in config_data.items():
            file.write(f"{key}\t{value}\n")


def rlc_render(
    rlc,
    configFile,
    inputImages,
    outputFolder,
    calibFile,
    startFrame,
    frames,
    viewNum,
    logFilePath,
):
    # Configure logging to write to logfilePath
    logging.basicConfig(
        filename=logFilePath,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Log the start of the task
    logging.info(
        f"[LVC TEST]: RLC rendering started for config: {configFile} with input images: {inputImages}, output folder: {outputFolder}, calibration file: {calibFile}, view number: {viewNum}\n"
    )

    try:
        # Update the configuration file before rendering
        updateConfig(
            configFile,
            inputImages,
            outputFolder,
            startFrame,
            frames,
            calibFile,
            viewNum,
        )

        # Run the RLC render process
        subprocess.run([rlc, configFile], check=True)

        # Log the successful completion of the task
        logging.info(
            f"[LVC TEST]: RLC rendering completed successfully for config: {configFile}\n\n"
        )

    except subprocess.CalledProcessError as e:
        # Log the error if subprocess fails
        logging.error(
            f"[LVC TEST]: RLC rendering failed for config: {configFile}. Error: {str(e)}\n\n"
        )
