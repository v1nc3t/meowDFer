import pytest

from PIL import Image
from src.utils import utils_pdfs

@pytest.fixture
def temp_dirs(tmp_path):
    src = tmp_path / "src"
    dest = tmp_path / "dest"

    src.mkdir()
    return src, dest

def test_convert_all_to_pdf(temp_dirs):
    src, dest = temp_dirs

    folder = src / "Chapter 1"
    folder.mkdir()

    for i in range(3):
        Image.new('RGB', (100, 100), color=(i*50, i*50, i*50)).save(folder / f"{i+1}.png")
    
    utils_pdfs.convert_all_to_pdf(str(src), str(dest), "Test")

    pdf_files = list(dest.glob("*.pdf"))

    assert len(pdf_files) == 1
    assert "Test Chapter 1.0.pdf" == pdf_files[0].name
    