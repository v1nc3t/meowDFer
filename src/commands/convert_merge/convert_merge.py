import os
import tempfile

from ..convert import convert_pdf
from ..merge import merge_pdf


def run(src, dest, vols, name, console):
    with tempfile.TemporaryDirectory() as temp_converted:
        if not convert_pdf.run(src, temp_converted, name, console):
            return False
        return merge_pdf.run(temp_converted, dest, vols, name, console)
