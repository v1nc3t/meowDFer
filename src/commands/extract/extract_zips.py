import os
import shutil
import tempfile
from typing import Any

from ...utils.file_utils import get_compressed_files

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
    if to_skip:
        log_skip = lambda f: console.print(f"[bold yellow]Skipped:[/bold yellow] unsupported compressed file fromat {f}")
    else:
        log_skip = lambda f: console.print(f"[bold red]Error:[/bold red] unsupported compressed file fromat {f}")

    try:
        zip_files = get_compressed_files(src_path, on_skip=log_skip)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        return False

    os.makedirs(dest_path, exist_ok=True)
    for file_name in zip_files:
        archive_path = os.path.join(src_path, file_name)
        try:
            shutil.unpack_archive(archive_path, extract_dir=dest_path)

            console.print(f"[blue]Staged:[/blue] {file_name}")
        except Exception as e:
            if to_skip:
                console.print(f"[bold yellow]Skipped:[/bold yellow] {file_name} due to error: {e}")
                continue

            console.print(f"[bold red]Failed to process {file_name}:[/bold red] {e}")
            return False

    return True
