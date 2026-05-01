import os
import tempfile

from rich.console import Console
from ..extract import extract_zips
from ..convert import convert_pdf
from ..merge import merge_pdf   

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
console = Console()

def run(src, dest, vols, name, console):
    with tempfile.TemporaryDirectory() as temp_extracted:
        extract_zips.run(src, temp_extracted, to_skip=True, console=console)

        with tempfile.TemporaryDirectory() as temp_converted:
            convert_pdf.run(temp_extracted, temp_converted, name, console)

            merge_pdf.run(temp_converted, dest, vols, name, console)

    