import subprocess
import os


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



if __name__ == "__main__":
    basePath = "/home/zrb/project/tsinghua-codec-experiment/agnostic-tools-python"
    file1 = os.path.join(basePath, "./data/raw/Boys.yuv")
    file2 = os.path.join(basePath, "./data/postproc/Boys_3976x2956_merged.yuv")
    # file2 = os.path.join(basePath, "./data/raw/Boys_output.yuv")
    psnr_y, psnr_u, psnr_v = compute_psnr_for_yuv(file1, file2, 3976, 2956)
    print(f"PSNR (Y): {psnr_y}")
    print(f"PSNR (U): {psnr_u}")
    print(f"PSNR (V): {psnr_v}")