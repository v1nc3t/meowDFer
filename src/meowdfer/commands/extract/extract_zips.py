import os
import shutil
import tempfile
import contextlib
from typing import Any

import patoolib
from patoolib.util import PatoolError

from meowdfer.utils.file_utils import get_compressed_files

def run(src_path: str, dest_path: str, to_skip: bool = False, console: Any = None) -> bool:
    with tempfile.TemporaryDirectory() as temp_dir:
        if not extract(src_path, temp_dir, to_skip, console):
            return False

        os.makedirs(dest_path, exist_ok=True)
        for item in os.listdir(temp_dir):
            s = os.path.join(temp_dir, item)
            d = os.path.join(dest_path, item)

            if os.path.exists(d) and os.path.isdir(d):
                shutil.rmtree(d)
            shutil.move(s, d)

    console.print(f"[bold green]Success:[/bold green] all files extraced")
    return True

def extract(src_path: str, dest_path: str, to_skip: bool, console: Any) -> bool:
    try:
        zip_files = get_compressed_files(src_path)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        return False

    os.makedirs(dest_path, exist_ok=True)
    for file_name in zip_files:
        archive_path = os.path.join(src_path, file_name)
        try:
            patoolib.extract_archive(archive_path, outdir=dest_path, verbosity=-1)

            console.print(f"[blue]Staged:[/blue] {file_name}")
        
        except PatoolError as e:
            error_msg = str(e)
            if "returned non-zero exit status" in error_msg:
                error_msg = "Archive is corrupt or cannot be opened by the system sub-program."

            if to_skip:
                console.print(f"[bold yellow]Skipped:[/bold yellow] {file_name}, {error_msg}")
                continue
            console.print(f"[bold red]Error:[/bold red]{file_name}, {error_msg}")
            return False
        
        except Exception as e:
            if to_skip:
                if console:
                    console.print(f"[bold yellow]Skipped:[/bold yellow] {file_name}, {e}")
                continue
            if console:
                console.print(f"[bold red]Error:[/bold red]{file_name}, {e}")
            return False

    return True
