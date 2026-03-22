import os
import shutil
import tempfile

from pypdf import PdfWriter
from rich.console import Console
from ...utils import naming_utils

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
console = Console()

def run(src, dest, vols, name):
    src_path = os.path.join(PROJECT_ROOT, src)
    dest_path = os.path.join(PROJECT_ROOT, dest)
    vols_path = os.path.join(PROJECT_ROOT, vols)

    with tempfile.TemporaryDirectory() as temp_path:
        try:
            # validate vols and src
            if not os.path.isfile(vols_path):
                raise FileNotFoundError(f"Volume intervals file not found: {vols_path}")
            
            with open(vols_path) as f:
                raw_data = f.read().replace('\n', '').split(",")
                intervals = [int(i.strip()) for i in raw_data if i.strip()]

            if not intervals or intervals != sorted(intervals):
                raise ValueError("Volume intervals must be a non-empty, strictly increasing list.")
            
            if not os.path.isdir(src_path):
                raise FileNotFoundError(f"Source folder not found: {src_path}")
            
            pdfs = [f for f in os.listdir(src_path) if f.lower().endswith(".pdf")]
            if not pdfs:
                raise ValueError("No PDF files found in source folder.")
            
            # mapping chapters
            pdfs = sorted(pdfs, key=naming_utils.extract_chapter_number)
            chapter_map = {}
            for f in pdfs:
                ch = naming_utils.extract_chapter_number(f)
                if ch in chapter_map:
                    raise ValueError(f"Duplicate chapter detected: {ch}.")
                chapter_map[ch] = f

            # staging into temp
            vol_num = 1
            prev = 0
            for val in intervals:
                start_ch, end_ch = prev + 1, val
        
                if start_ch > end_ch:
                    raise ValueError(f"Invalid volume range: {start_ch} -> {end_ch}.")

                merger = PdfWriter()
                vol_name = naming_utils.create_volume_name(name, vol_num) + ".pdf"
                temp_vol_path = os.path.join(temp_path, vol_name)

                for ch in range(start_ch, end_ch + 1):
                    if ch not in chapter_map:
                        raise ValueError(f"Missing chapter {ch} for Volume {vol_num}.")
                    merger.append(os.path.join(src_path, chapter_map[ch]))
            
                with open(temp_vol_path, "wb") as f_out:
                    merger.write(f_out)
                merger.close()

                console.print(f" [blue]Staged:[/blue] {vol_name} (Chapters {start_ch}-{end_ch})")
                vol_num += 1
                prev = val
            
            # commit into destination
            os.makedirs(dest_path, exist_ok=True)
            
            staged_files = os.listdir(temp_path)
            if not staged_files:
                raise ValueError("No volumes were staged. Nothing to move.")
        
            for file_name in staged_files:
                shutil.move(
                    os.path.join(temp_path, file_name), 
                    os.path.join(dest_path, file_name)
                )
            
            console.print(f"\n[bold green]All volumes merged successfully to:[/bold green] {dest_path}\n")
        except Exception as e:
            console.print(f"\n[bold red]Merge Aborted:[/bold red] {e}.")