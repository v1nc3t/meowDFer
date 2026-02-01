import os

from PIL import Image
from pypdf import PdfWriter

from .import utils_naming as u_name 

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def convert_all_to_pdf(src, dest, name):
    src = os.path.join(PROJECT_ROOT, src)
    dest = os.path.join(PROJECT_ROOT, dest)

    if not os.path.isdir(src):
        raise FileNotFoundError(f"Source folder not found: {src}")

    os.makedirs(dest, exist_ok=True)

    for folder in os.listdir(src):
        path = os.path.join(src, folder)
        if os.path.isdir(path):
            try:
                convert_folder_to_pdf(path, dest, name)
            except Exception as e:
                print(f"Failed to convert folder `{folder}`: {e}")

    print("All folders converted to PDFs")

def convert_folder_to_pdf(src, dest, name):
    folder_name = os.path.basename(src.rstrip('/'))
    
    try:
        chapter_number = u_name.extract_chapter_number(folder_name)
    except ValueError as e:
        print(f"Skipping folder: {folder_name}: {e}")
        return

    pdf_name = u_name.create_chapter_name(name, chapter_number) + ".pdf"
    pdf_path = os.path.join(dest, pdf_name)

    try:
        images = sorted(
            [f for f in os.listdir(src) if f.endswith((".png", ".jpg", ".jpeg"))],
            key=u_name.extract_page_number
        )
    except Exception as e:
        raise RuntimeError(f"Failed to sort images in {src}")
    
    if not images:
        print(f"No images found in folder")
        return

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
        print(f"No valid image in folder: {src}")
        return

    first_img = img_list.pop(0)
    first_img.save(pdf_path, save_all=True, append_images=img_list)
    
    print(f"PDF created: {pdf_name}")

def merge_to_volumes(src, dest, name):
    src = os.path.join(PROJECT_ROOT, src)
    dest = os.path.join(PROJECT_ROOT, dest)

    if not src:
        raise FileNotFoundError(f"Source folder no found: {src}")
    
    os.makedirs(dest, exist_ok=True)

    merger = PdfWriter()

    file = sorted(
        [f for f in os.listdir(src) if f.endswith(".pdf")],
        key=u_name.extract_chapter_number
    )
    for pdf in file:
        pdf_path = os.path.join(src, pdf)
        merger.append(pdf_path)
        print(f"Added to merge: `{pdf}`")

    name = f"{name} Vol.{1}.pdf"
    output_path = os.path.join(dest, name)
    with open(output_path, "wb") as output:
        merger.write(output)
    
    merger.close()

    print(f"Finished merge")

