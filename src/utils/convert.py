import os

from PIL import Image

from . import utils_naming as u_name

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def convert_all_to_pdf(src, dest, name):
    print("\n\033[95mRunning convert...\033[0m\n")
    
    src = os.path.join(PROJECT_ROOT, src)
    dest = os.path.join(PROJECT_ROOT, dest)

    if not os.path.isdir(src):
        raise FileNotFoundError(f"\033[91mSource folder not found:\033[0m {src}")

    os.makedirs(dest, exist_ok=True)

    for folder in os.listdir(src):
        path = os.path.join(src, folder)
        if os.path.isdir(path):
            try:
                convert_folder_to_pdf(path, dest, name)
            except Exception as e:
                print(f"\033[91mFailed to convert folder `{folder}`:\033[0m {e}")

    print("\n\033[95mAll folders converted to PDFs\033[0m\n")

def convert_folder_to_pdf(src, dest, name):
    folder_name = os.path.basename(src.rstrip('/'))
    
    try:
        chapter_number = u_name.extract_chapter_number(folder_name)
    except ValueError as e:
        print(f"\033[93mSkipping folder {folder_name}:\033[0m {e}")
        return

    pdf_name = u_name.create_chapter_name(name, chapter_number) + ".pdf"
    pdf_path = os.path.join(dest, pdf_name)

    try:
        images = sorted(
            [f for f in os.listdir(src) if f.endswith((".png", ".jpg", ".jpeg"))],
            key=u_name.extract_page_number
        )
    except Exception as e:
        raise RuntimeError(f"\033[91mFailed to sort images in {src}\033[0m")
    
    if not images:
        print(f"\033[91mNo images found in folder\033[0m")
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
            print(f"\033[93mSkipping image `{image}`:\033[0m {e}")

    if not img_list:
        print(f"\033[91mNo valid image in folder:\033[0m {src}")
        return

    first_img = img_list.pop(0)
    first_img.save(pdf_path, save_all=True, append_images=img_list)
    
    print(f"\033[92mPDF created:\033[0m {pdf_name}")