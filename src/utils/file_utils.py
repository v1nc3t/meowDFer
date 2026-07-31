import os
from functools import partial
from .naming_utils import extract_chapter_number, extract_page_number, extract_volume_number

def get_compressed_files(src: str) -> list[str]:
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory not found: {src}")

    valid_exts = (
        ".zip", ".cbz", ".rar", ".cbr", ".tar", ".tgz",
        ".gz", ".bz2", ".xz"
    )
    
    files = []
    for f in os.listdir(src):
        full_path = os.path.join(src, f)
        if os.path.isfile(full_path) and f.lower().endswith(valid_exts):
            files.append(f)
    
    if not files:
        raise ValueError(f"No supported compressed files found in directory: {src}")

    return files

def get_folders(src: str) -> list[str]:
    if not os.path.isdir(src):
        raise FileNotFoundError(f"Source directory not found: {src}")

    folders = [f for f in os.listdir(src) if os.path.isdir(os.path.join(src, f))]

    if not folders:
        raise ValueError(f"No folders found in directory: {src}")
    
    return folders
    
def sort_chapters(files: list[str], allow_decimal: bool) -> list[str]:
    if not files:
        raise ValueError("No folders found to sort.")
    
    key_func = partial(extract_chapter_number, allow_decimal=allow_decimal)
    
    for f in files:
        try:
            key_func(f)
        except ValueError as e:
            raise ValueError(f"Sorting aborted: Malformed chapter folder structure. Details: {e}")

    return sorted(files, key=key_func)

def sort_volumes(files: list[str]) -> list[str]:
    if not files:
        raise ValueError("No folders found to sort.")
    
    return sorted(
        files,
        key=lambda f: (extract_volume_number(f), f)
    )

def get_images(src: str) -> list[str]:
    if not os.path.isdir(src):
        raise FileNotFoundError(f"Source directory not found: {src}")
    
    images = [f for f in os.listdir(src) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]

    if not images:
        raise ValueError(f"No images found in directory: {src}")
    
    return images

def sort_page_number(files: list[str]) -> list[str]:
    if not files:
        raise ValueError("No files found.")

    return sorted(
        files, 
        key=lambda f: (extract_page_number(f), f)
    )

def get_pdfs(src: str) -> list[str]:
    if not os.path.isdir(src):
        raise FileNotFoundError(f"Source directory not found: {src}")
    
    pdfs = [f for f in os.listdir(src) if f.lower().endswith(".pdf")]

    if not pdfs:
        raise ValueError("No PDF files found.")
    
    return pdfs
    
def get_volumes_file(src: str) -> list[int]:
    if not os.path.isfile(src):
        raise FileNotFoundError(f"Volume intervals file not found: {src}")

    with open(src) as f:
        raw_data = f.read().replace('\n', '').split(",")
        intervals = [int(i.strip()) for i in raw_data if i.strip()]

    if not intervals:
        raise ValueError("Volume intervals must be a non-empty list")
    
    if intervals != sorted(intervals):
        raise ValueError("Volume intervals must be a strictly increasing list")
    
    return intervals

def get_chapter_map(files: list[str], allow_decimal: bool) -> dict[float | int, str]:
    chapter_map: dict[float | int, str] = {}

    for f in files:
        try:
            ch = extract_chapter_number(f, allow_decimal)
        except ValueError as e:
            raise ValueError(f"Failed to build chapter map. Extraction error on file '{f}': {e}")

        if ch in chapter_map:
            raise ValueError(
                f"Duplicate chapter detected: {ch}. "
                f"Conflict between current file '{f}' and existing entry '{chapter_map[ch]}'."
            )
        
        chapter_map[ch] = f
    
    return chapter_map