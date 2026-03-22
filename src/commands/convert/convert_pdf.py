import os
import shutil
import tempfile

from PIL import Image
from rich.console import Console
from ...utils import naming_utils

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
console = Console()

def run(src, dest, name):
    src_path = os.path.join(PROJECT_ROOT, src)
    dest_path = os.path.join(PROJECT_ROOT, dest)

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            if not os.path.isdir(src_path):
                raise FileNotFoundError(f"Source folder not found: {src_path}")

            folders = [f for f in os.listdir(src_path) if os.path.isdir(os.path.join(src_path, f))]

            if not folders:
                raise ValueError("No folders found in given source folder")
            
            folders = sorted(folders, key=naming_utils.extract_chapter_number)

            for folder in folders:
                folder_path = os.path.join(src_path, folder)

                convert_folder_to_pdf(folder_path, temp_dir, name)
            
            os.makedirs(dest_path, exist_ok=True)
            for file_name in os.listdir(temp_dir):
                shutil.move(
                    os.path.join(temp_dir, file_name), 
                    os.path.join(dest_path, file_name)
                )
            
            console.print(f"[bold green]All folders converted successfully to:[/bold green] {dest_path}")

        except Exception as e:
            console.print(f"\n[bold red]Conversion Aborted:[/bold red] {e}")

def convert_folder_to_pdf(src, dest, name):
    folder_name = os.path.basename(src.rstrip('/'))
    
    try:
        chapter_number = naming_utils.extract_chapter_number(folder_name)
    except ValueError as e:
        print(f"Skipping folder {folder_name}: {e}")
        return

    pdf_name = naming_utils.create_chapter_name(name, chapter_number) + ".pdf"
    pdf_path = os.path.join(dest, pdf_name)

    try:
        images = sorted(
            [f for f in os.listdir(src) if f.endswith((".png", ".jpg", ".jpeg"))],
            key=naming_utils.extract_page_number
        )
    except Exception as e:
        raise RuntimeError(f"Failed to sort images in {src}.")
    
    if not images:
        raise ValueError(f"No images found in folder.")

    img_list = []
    for image in images:
        img_path = os.path.join(src, image)
        try:
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_list.append(img)
        except Exception as e:
            print(f"Skipping image `{image}`: {e}")

    if not img_list:
        raise ValueError(f"No valid images in folder: {src}")

    first_img = img_list.pop(0)
    first_img.save(pdf_path, save_all=True, append_images=img_list)
    
    console.print(f" [blue]Staged:[/blue] {pdf_name}")