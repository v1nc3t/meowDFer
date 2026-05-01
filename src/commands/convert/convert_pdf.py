import os
import shutil
import tempfile

from PIL import Image
from rich.console import Console
from ...utils.naming_utils import extract_chapter_number, create_chapter_name
from ...utils.file_utils import get_folders, sort_folders_chapters, get_images, sort_page_number

def run(src_path, dest_path, name, console):
    with tempfile.TemporaryDirectory() as temp_dir:
        convert(src_path, dest_path, name, console)

        # move from temp to dest
        os.makedirs(dest_path, exist_ok=True)

        for item in os.listdir(temp_dir):
            s = os.path.join(temp_dir, item)
            d = os.path.join(dest_path, item)

            if os.path.exists(d) and os.path.isdir(d):
                shutil.rmtree(d)
            shutil.move(s, d)

def convert(src_path, dest_path, name, console):
    try:
        folders = get_folders(src_path)
        sorted_folders = sort_folders_chapters(folders)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return

    for folder in sorted_folders:
        folder_path = os.path.join(src_path, folder)

        try:
            convert_folder_to_pdf(folder_path, dest_path, name, console)
        except Exception as e:
            console.print(f"[bold red]Failed to process {folder}:[/bold red] {e}")
            return

def convert_folder_to_pdf(src, dest, name, console):
    folder_name = os.path.basename(src.rstrip('/'))
    
    chapter_number = extract_chapter_number(folder_name)
    
    pdf_name = create_chapter_name(name, chapter_number) + ".pdf"
    pdf_path = os.path.join(dest, pdf_name)

    try:
        images = get_images(src)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return
    
    sorted_images = sort_page_number(images)

    img_list = []
    for image in sorted_images:
        img_path = os.path.join(src, image)
        try:
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_list.append(img)
        except Exception as e:
            raise RuntimeError(f"Could not process {image}: {e}")

    if not img_list:
        raise ValueError(f"No valid images in folder: {src}")

    first_img = img_list.pop(0)
    first_img.save(pdf_path, save_all=True, append_images=img_list)
    
    console.print(f" [blue]Staged:[/blue] {pdf_name}")