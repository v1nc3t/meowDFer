import os
import shutil
import tempfile

from zipfile import ZipFile, BadZipFile
from rich.console import Console

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
console = Console()

def run(src_path, dest_path):
    src_path = os.path.join(PROJECT_ROOT, src_path)
    dest_path = os.path.join(PROJECT_ROOT, dest_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            if not os.path.exists(src_path):
                raise FileNotFoundError(f"Source directory not found: {src_path}")

            zip_files = [f for f in os.listdir(src_path) if f.endswith(".zip")]

            if not zip_files:
                console.print("[yellow]No zip files found to extract.[/yellow]")
                return
            
            # extraction 
            for file_name in zip_files:
                zip_path = os.path.join(src_path, file_name)
                with ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                console.print(f"[green]Prepared:[/green] {file_name}")

            # move from temp to dest
            os.makedirs(dest_path, exist_ok=True)

            for item in os.listdir(temp_dir):
                s = os.path.join(temp_dir, item)
                d = os.path.join(dest_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            
            console.print(f"Files are now in: [cyan]{dest_path}[/cyan]\n")
        except Exception as e:
            console.print(f"\n[bold red]Extraction Aborted:[/bold red] {e}")
            console.print("[yellow]The destination folder remains untouched.[/yellow]\n")