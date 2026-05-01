import os
import tempfile

from rich.console import Console
from ..convert import convert_pdf
from ..merge import merge_pdf   

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
console = Console()

def run(src, dest, vols, name, console):
    with tempfile.TemporaryDirectory() as temp_converted:
        convert_pdf.run(src, temp_converted, name=name)

        merge_pdf.run(temp_converted, dest, vols, name, console)