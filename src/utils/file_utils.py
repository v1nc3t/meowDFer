import os

from .naming_utils import extract_chapter_number, extract_page_number

def get_zip_files(src):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory not found: {src}")

    files = [f for f in os.listdir(src) if f.endswith(".zip")]
    
    if not files:
        raise ValueError(f"No zip files found in directory: {src}")

    return files

def get_folders(src):
    if not os.path.isdir(src):
        raise FileNotFoundError(f"Source directory not found: {src}")

    folders = [f for f in os.listdir(src) if os.path.isdir(os.path.join(src, f))]

    if not folders:
        raise ValueError(f"No folders found in directory: {src}")
    
    return folders
    
def sort_folders_chapters(folders):
    if not folders:
        raise ValueError(f"No folders found to sort.")
    
    sorted_folders = sorted(
        (f for f in folders if extract_chapter_number(f) is not None),
        key=extract_chapter_number
    )

    return sorted_folders

def get_images(src):
    if not os.path.isdir(src):
        raise FileNotFoundError(f"Source directory not found: {src}")
    
    images = [f for f in os.listdir(src) if f.endswith((".png", ".jpg", ".jpeg"))]

    if not images:
        raise ValueError(f"No images found in directory: {src}")
    
    return images

def sort_page_number(files):
    if not files:
        raise ValueError(f"No files found.")

    sorted_files = sorted(
        files, key=extract_page_number
    )

    return sorted_files
