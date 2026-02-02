import os

from pypdf import PdfWriter

from . import utils_naming as u_name 

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def merge_to_volumes(src, dest, vals, name):
    print("\n\033[95mRunning merge...\033[0m\n")

    src = os.path.join(PROJECT_ROOT, src)
    dest = os.path.join(PROJECT_ROOT, dest)
    vals = os.path.join(PROJECT_ROOT, vals)

    if not os.path.isdir(src):
        raise FileNotFoundError(f"\033[91mSource folder no found:\033[0m {src}")
    
    if not os.path.isfile(vals):
        raise FileNotFoundError(f"\033[91mIntervals file not found:\033[0m {vals}")
    
    os.makedirs(dest, exist_ok=True)

    try:
        with open(vals) as f:
            intervals = list(map(int, f.read().split(", ")))
    except:
        raise ValueError("\033[91mInterval file must contain only integers separated by ', '\033[0m")

    if not intervals:
        raise ValueError("\033[91mIntervals list is empty\033[0m")
    
    if intervals != sorted(intervals):
        raise ValueError("\033[91mIntervals must be stricty increasing\033[0m")

    pdfs = [f for f in os.listdir(src) if f.endswith(".pdf")]

    if not pdfs:
        raise ValueError("\033[91mNo PDF files found in given source folder\033[0m")
    
    pdfs = sorted(pdfs, key=u_name.extract_chapter_number)

    chapter_map = {}
    for f in pdfs:
        ch = u_name.extract_chapter_number(f)
        if ch in chapter_map:
            raise ValueError(f"\033[91mDuplicate chapter detected:\033[0m {ch}")
        chapter_map[ch] = f

    vol_num = 1
    prev = 0
    for val in intervals:
        start_ch = prev + 1
        end_ch = val

        if start_ch > end_ch:
            raise ValueError(f"\033[91mInvalid volume range:\033[0m {start_ch} -> {end_ch}")

        merger = PdfWriter()
        try:    
            for ch in range(start_ch, end_ch + 1):
                if ch not in chapter_map:
                    raise ValueError(f"\033[91mMissing chapter:\033[0m {ch}")
                merger.append(os.path.join(src, chapter_map[ch]))
                print(f"\033[96mAdded to merge:\033[0m `{chapter_map[ch]}`")
            
            vol_name = u_name.create_volume_name(name, vol_num) + ".pdf"
            vol_path = os.path.join(dest, vol_name)
            
            with open(vol_path, "wb") as vol:
                merger.write(vol)
            
            print(f"\n\033[92mMerge succesful:\033[0m `{vol_name}`\n")
        finally:
            merger.close()

        vol_num += 1
        prev = val

    print(f"\033[95mFinished merge\033[0m\n")