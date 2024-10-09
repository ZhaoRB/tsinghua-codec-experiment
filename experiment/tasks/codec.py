import subprocess


def vvc_codec(
    app, input, output_bitstream, output_yuv, cfgFile, width, height, frames, qp
):
    subprocess.run(
        [
            app,
            "-c",
            cfgFile,
            "-wdt",
            width,
            "-hgt",
            height,
            "-fr",
            30,  # Frame rate
            "--InputBitDepth=8",
            "--OutputBitDepth=8",
            f"--FramesToBeEncoded={frames}",
            "--Level=6.2",
            "--ConformanceMode=1",
            f"--QP={qp}",
            "-i",
            input,
            "-b",
            output_bitstream,  # Bitstream output file name
            "-o",
            output_yuv,  # Reconstructed YUV output file name
        ]
    )
