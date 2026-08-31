import os
import math
import shutil
import tempfile
from typing import Any

from pypdf import PdfWriter
from meowdfer.utils import naming_utils
from meowdfer.utils.file_utils import get_pdfs, sort_chapters, get_volumes_file, get_chapter_map, split_valid_chapters


def run(src_path: str, dest_path: str, vols_path: str, name: str, to_skip: bool = False, console: Any = None) -> bool:
    with tempfile.TemporaryDirectory() as temp_dir:
        if not merge(src_path, temp_dir, vols_path, name, to_skip, console):
            return False

        os.makedirs(dest_path, exist_ok=True)
        for item in os.listdir(temp_dir):
            s = os.path.join(temp_dir, item)
            d = os.path.join(dest_path, item)

            if os.path.exists(d) and os.path.isdir(d):
                shutil.rmtree(d)
            shutil.move(s, d)

    console.print(f"[bold green]Success:[/bold green] all files merged")
    return True


def merge(src: str, dest: str, vols: str, name: str, to_skip: bool, console: Any) -> bool:
    try:
        pdfs = get_pdfs(src)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        return False

    pdfs, invalid = split_valid_chapters(pdfs)
    for bad_name, err in invalid:
        if not to_skip:
            console.print(
                f"[bold red]Initialization Error:[/bold red] Sorting aborted: Malformed chapter folder structure. Details: {err}"
            )
            return False
        console.print(f"[bold yellow]Skipped:[/bold yellow] {bad_name}, {err}")

    try:
        sorted_pdfs = sort_chapters(pdfs)
        intervals = get_volumes_file(vols)
        chapter_map = get_chapter_map(sorted_pdfs)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        return False

    vol_num = 1
    prev = 0

    for val in intervals:
        start_ch, end_ch = prev + 1, val
        vol_name = naming_utils.create_volume_name(name, vol_num) + ".pdf"
        
        if start_ch > end_ch:
            console.print(f"[bold red]Alignment Error:[/bold red] Volume {vol_num} range invalid ({start_ch}-{end_ch})")
            return False
        
        chapters_in_this_vol = []
        for ch_num in sorted(chapter_map.keys()):
            base_ch = math.floor(ch_num)
            if start_ch <= base_ch <= end_ch:
                chapters_in_this_vol.append(ch_num)
        
        missing_chapters = []
        for exact_ch in range(start_ch, end_ch + 1):
            if not any(math.floor(k) == exact_ch for k in chapter_map.keys()):
                missing_chapters.append(exact_ch)

        if missing_chapters:
            msg = f"Chapters {missing_chapters} missing completely for volume {vol_num}"
            if to_skip:
                console.print(f"[bold yellow]Skipped:[/bold yellow] volume {vol_num}, missing core chapters.")
                vol_num += 1
                prev = val
                continue

            console.print(f"[bold red]Data Error:[/bold red] volume {vol_num} is missing chapters: {missing_chapters}")
            return False
        
        if not chapters_in_this_vol:
            if to_skip:
                console.print(f"[bold yellow]Skipped:[/bold yellow] volume {vol_num} has no matching files in range {start_ch}-{end_ch}.")
                vol_num += 1
                prev = val
                continue
            
            console.print(f"[bold red]Data Error:[/bold red] volume {vol_num} has no matching files in range {start_ch}-{end_ch}.")
            return False

        try:
            merger = PdfWriter()
            temp_vol_path = os.path.join(dest, vol_name)

            for ch_num in chapters_in_this_vol:
                file_path = os.path.join(src, chapter_map[ch_num])
                merger.append(file_path)

            with open(temp_vol_path, "wb") as f_out:
                merger.write(f_out)
            merger.close()

            console.print(f"[blue]Staged:[/blue] {vol_name} (Chapters {start_ch}-{end_ch})")

        except Exception as e:
            if to_skip:
                console.print(f"[bold yellow]Skipping:[/bold yellow] {vol_name} due to error: {e}")
                
                vol_num += 1
                prev = val
                continue

            console.print(f"[bold red]Failed to process {vol_name}:[/bold red] {e}")
            return False

        vol_num += 1
        prev = val

    return True
