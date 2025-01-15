import subprocess


def compute_psnr_for_yuv(file1, file2, width, height):
    # Construct the ffmpeg command to calculate PSNR
    command = [
        "ffmpeg",
        "-s",
        f"{width}x{height}",
        "-pix_fmt",
        "yuv420p",
        "-i",
        file1,
        "-s",
        f"{width}x{height}",
        "-pix_fmt",
        "yuv420p",
        "-i",
        file2,
        "-lavfi",
        "psnr",
        "-f",
        "null",
        "-",
    ]

    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Default PSNR values
    psnr_y, psnr_u, psnr_v = None, None, None

    # Extract PSNR values from the output
    output = result.stderr  # PSNR information is typically outputted to stderr
    for line in output.splitlines():
        if "PSNR y:" in line:
            try:
                # Split the line by spaces and colons to extract the values
                psnr_y = float(line.split("PSNR y:")[1].split()[0])
                psnr_u = float(line.split("u:")[1].split()[0])
                psnr_v = float(line.split("v:")[1].split()[0])
            except (IndexError, ValueError) as e:
                print(f"Error parsing PSNR values from ffmpeg output: {e}")
            break  # Stop after finding the PSNR line

    if psnr_y is None or psnr_u is None or psnr_v is None:
        raise ValueError("Failed to calculate PSNR values from ffmpeg output.")

    return psnr_y, psnr_u, psnr_v
