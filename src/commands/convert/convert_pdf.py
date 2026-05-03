import os
import shutil
import tempfile

from PIL import Image
from ...utils.naming_utils import extract_chapter_number, create_chapter_name
from ...utils.file_utils import get_folders, sort_chapters, get_images, sort_page_number


def run(src_path, dest_path, name, console):
    with tempfile.TemporaryDirectory() as temp_dir:
        if not convert(src_path, temp_dir, name, console):
            return False

        os.makedirs(dest_path, exist_ok=True)
        for item in os.listdir(temp_dir):
            s = os.path.join(temp_dir, item)
            d = os.path.join(dest_path, item)

            if os.path.exists(d) and os.path.isdir(d):
                shutil.rmtree(d)
            shutil.move(s, d)

    return True


def convert(src_path, dest_path, name, console):
    try:
        folders = get_folders(src_path)
        sorted_folders = sort_chapters(folders)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return False

    for folder in sorted_folders:
        folder_path = os.path.join(src_path, folder)
        folder_name = os.path.basename(folder_path.rstrip("/"))

        try:
            chapter_number = extract_chapter_number(folder_name, False)
        except ValueError as e:
            console.print(f"[bold yellow]Skipped:[/bold yellow] {e}")
            continue

        try:
            pdf_name = convert_folder_to_pdf(folder_path, dest_path, chapter_number, name, console)
            console.print(f"[blue]Staged:[/blue] {pdf_name}")
        except Exception as e:
            console.print(f"[bold red]Failed to process {folder}:[/bold red] {e}")
            return False

    return True


def convert_folder_to_pdf(src, dest, chapter_number, name, console):
    pdf_name = create_chapter_name(name, chapter_number) + ".pdf"
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
