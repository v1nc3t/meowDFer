import os
import tempfile

from ..extract import extract_zips
from ..convert import convert_pdf
from ..merge import merge_pdf

def run(src, dest, vols, name, to_skip, console):
    with tempfile.TemporaryDirectory() as temp_extracted:
        if not extract_zips.run(src, temp_extracted, to_skip, console=console):
            return False

        with tempfile.TemporaryDirectory() as temp_converted:
            if not convert_pdf.run(temp_extracted, temp_converted, name, to_skip, console):
                return False
            return merge_pdf.run(temp_converted, dest, vols, name, to_skip, console)
