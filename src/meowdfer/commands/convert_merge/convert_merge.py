import os
import tempfile
from typing import Any

from ..convert import convert_pdf
from ..merge import merge_pdf

def run(src: str, dest: str, vols: str, name: str, folder_type: str, allow_decimal: bool = False, to_skip: bool = False, console: Any = None) -> bool:
    with tempfile.TemporaryDirectory() as temp_converted:
        if not convert_pdf.run(src, temp_converted, name, folder_type, allow_decimal, to_skip, console):
            return False
        return merge_pdf.run(temp_converted, dest, vols, name, allow_decimal, to_skip, console)
