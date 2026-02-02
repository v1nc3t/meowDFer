import os

from pypdf import PdfWriter

from . import utils_naming as u_name 

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def merge_to_volumes(src, dest, intervals, name):
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