import os
import shutil
import tempfile
from typing import Any

from PIL import Image
from utils.naming_utils import extract_chapter_number, extract_volume_number, create_chapter_name, create_volume_name
from utils.file_utils import get_folders, sort_chapters, sort_volumes, get_images, sort_page_number


def run(src_path: str, dest_path: str, name: str, folder_type: str, allow_decimal: bool = False, to_skip: bool = False, console: Any = None) -> bool:
    with tempfile.TemporaryDirectory() as temp_dir:
        if not convert(src_path, temp_dir, name, folder_type, allow_decimal, to_skip, console):
            return False

        os.makedirs(dest_path, exist_ok=True)
        for item in os.listdir(temp_dir):
            s = os.path.join(temp_dir, item)
            d = os.path.join(dest_path, item)

            if os.path.exists(d) and os.path.isdir(d):
                shutil.rmtree(d)
            shutil.move(s, d)

    console.print(f"[bold green]Success:[/bold green] all files converted")
    return True


def convert(src_path: str, dest_path: str, name: str, folder_type: str, allow_decimal: bool, to_skip: bool, console: Any) -> bool:
    try:
        folders = get_folders(src_path)
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        return False

    try:
        if folder_type == "chapter":
            sorted_folders = sort_chapters(folders, allow_decimal=allow_decimal)
        else:
            sorted_folders = sort_volumes(folders)
    except ValueError as e:
        console.print(f"[bold red]Sorting Error:[/bold red] {e}")
        return False

    for folder in sorted_folders:
        folder_path = os.path.join(src_path, folder)
        folder_name = os.path.basename(folder_path.rstrip("/"))

        try:
            if folder_type == "chapter":
                chapter_number = extract_chapter_number(folder_name, allow_decimal)
                pdf_name = convert_folder_to_pdf(folder_path, dest_path, folder_type, chapter_number, name)

                console.print(f"[blue]Staged:[/blue] {pdf_name}")
            else:
                volume_number = extract_volume_number(folder_name)
                pdf_name = convert_folder_to_pdf(folder_path, dest_path, folder_type, volume_number, name)
            
                console.print(f"[blue]Staged:[/blue] {pdf_name}")

        except Exception as e:
            if to_skip:
                console.print(f"[bold yellow]Skipped: {folder_name} due to erorr: {e}[/bold yellow]")
                continue

            console.print(f"[bold red]Failed to process {folder_name}:[/bold red] {e}")
            return False

    return True


def convert_folder_to_pdf(src: str, dest: str, folder_type: str, number: int, name: str) -> str:
    if folder_type == "chapter":
        pdf_name = create_chapter_name(name, number) + ".pdf"
    else:
        pdf_name = create_volume_name(name, number) + ".pdf"

    pdf_path = os.path.join(dest, pdf_name)

    images = get_images(src)
    sorted_images = sort_page_number(images)

    img_list = []
    for image in sorted_images:
        img_path = os.path.join(src, image)
        try:
            img = Image.open(img_path)
            if img.mode != "RGB":
                img = img.convert("RGB")
            img_list.append(img)
        except Exception as e:
            raise RuntimeError(f"Could not process {image}: {e}") from e

    if not img_list:
        raise ValueError(f"No valid images in folder: {src}")

    first_img = img_list.pop(0)
    first_img.save(pdf_path, save_all=True, append_images=img_list)

    return pdf_name
