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
    
    os.makedirs(dest, exist_ok=True)

    with open(vals) as f:
        intervals = list(map(int, f.read().split(", ")))

    pdfs = sorted(
        [f for f in os.listdir(src) if f.endswith(".pdf")],
        key=u_name.extract_chapter_number
    )

    chapter_map = {
        u_name.extract_chapter_number(f): f
        for f in pdfs
    }

    vol_num = 1
    prev = 0
    for val in intervals:
        start_ch = prev + 1
        end_ch = val

        merger = PdfWriter()
        for ch in range(start_ch, end_ch + 1):
            ch_name = chapter_map[ch]
            ch_path = os.path.join(src, ch_name)
            merger.append(ch_path)
            print(f"Added to merge: `{ch_name}`")
        
        vol_name = u_name.create_volume_name(name, vol_num) + ".pdf"
        vol_path = os.path.join(dest, vol_name)
        
        with open(vol_path, "wb") as vol:
            merger.write(vol)
            print(f"Merge succesful: `{vol_name}`")
        
        merger.close()

        vol_num += 1
        prev = val

    print(f"Finished merge")