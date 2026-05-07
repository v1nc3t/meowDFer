import os
import shutil
import tempfile

from ...utils.file_utils import get_zip_files
from zipfile import ZipFile

def run(src_path, dest_path, to_skip, console):
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

    return True

def extract(src_path, dest_path, to_skip, console):
    try:
        zip_files = get_zip_files(src_path)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        return False

    os.makedirs(dest_path, exist_ok=True)
    for file_name in zip_files:
        zip_path = os.path.join(src_path, file_name)
        try:
            with ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(dest_path)
            console.print(f"[blue]Staged:[/blue] {file_name}")
        except Exception as e:
            if to_skip:
                console.print(f"[bold yellow]Skipped: {file_name} due to error: {e}[/bold yellow]")
                continue

            console.print(f"[bold red]Failed to process {file_name}:[/bold red] {e}")
            return False

    return True