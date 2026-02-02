import os

from pypdf import PdfWriter

from . import utils_naming as u_name 

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def merge_to_volumes(src, dest, vals, name):
    src = os.path.join(PROJECT_ROOT, src)
    dest = os.path.join(PROJECT_ROOT, dest)
    vals = os.path.join(PROJECT_ROOT, vals)

    if not os.path.isdir(src):
        raise FileNotFoundError(f"Source folder no found: {src}")
    
    if not os.path.isfile(vals):
        raise FileNotFoundError(f"Intervals file not found: {vals}")
    
    os.makedirs(dest, exist_ok=True)

    try:
        with open(vals) as f:
            intervals = list(map(int, f.read().split(", ")))
    except:
        raise ValueError("Interval file must contain only integers separated by ', '")

    if not intervals:
        raise ValueError("Intervals list empty")
    
    if intervals != sorted(intervals):
        raise ValueError("Intervals must be stricty increasing")

    pdfs = [f for f in os.listdir(src) if f.endswith(".pdf")]

    if not pdfs:
        raise ValueError("No PDF files foind in given source folder")
    
    pdfs = sorted(pdfs, key=u_name.extract_chapter_number)

    chapter_map = {}
    for f in pdfs:
        ch = u_name.extract_chapter_number(f)
        if ch in chapter_map:
            raise ValueError(f"Duplicate chapter detected: {ch}")
        chapter_map[ch] = f

    vol_num = 1
    prev = 0
    for val in intervals:
        start_ch = prev + 1
        end_ch = val

        if start_ch > end_ch:
            raise ValueError(f"Invalid volume range: {start_ch} -> {end_ch}")

        merger = PdfWriter()
        try:    
            for ch in range(start_ch, end_ch + 1):
                if ch not in chapter_map:
                    raise ValueError(f"Missing chapter: {ch}")
                merger.append(os.path.join(src, chapter_map[ch]))
                print(f"Added to merge: `{chapter_map[ch]}`")
            
            vol_name = u_name.create_volume_name(name, vol_num) + ".pdf"
            vol_path = os.path.join(dest, vol_name)
            
            with open(vol_path, "wb") as vol:
                merger.write(vol)
            
            print(f"Merge succesful: `{vol_name}`")
        finally:
            merger.close()

        vol_num += 1
        prev = val

    print(f"Finished merge")