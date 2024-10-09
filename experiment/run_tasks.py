from tasks.codec import vvc_codec
from tasks.format_convert import img2yuv, yuv2img
from tasks.mca import mca20_post, mca20_pre, mca_post, mca_pre
from tasks.render import rlc_render
from config import parseConfigFile


def run():
    config = parseConfigFile()

    