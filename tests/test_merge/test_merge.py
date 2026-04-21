import os
import io
import pytest

from pypdf import PdfWriter
from src.commands.merge.merge_pdf import run

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

@pytest.fixture
def temp_dirs(tmp_path):
    src = tmp_path / "src"
    dest = tmp_path / "dest"
    vols = tmp_path / "vols.txt"
    src.mkdir()
    return str(src), str(dest), str(vols)

def create_pdf(src_path, name):
    folder_path = os.path.join(src_path, name)

    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(folder_path, "wb") as f:
        writer.write(f)
    
    return folder_path

def create_corrupt_pdf(src_path, name):
    folder_path = os.path.join(src_path, name)

    writer = PdfWriter()
    with open(folder_path, "wb") as f:
        f.write(b"%PDF-1.4\n%%EOF_CORRUPT_DATA")
    
    return folder_path

def create_vols_file(src_path, content):
    with open(src_path, "w") as f:
        f.write(content)

# --- tests ---

def test_merge_bad_source(temp_dirs):
    src_path, dest_path, vols_path = temp_dirs

    with pytest.raises(FileNotFoundError) as excinfo:
        run("src_bad", dest_path, vols_path, "test")
    
    assert not os.path.isdir(dest_path)

def test_merge_empty_source(temp_dirs):
    src_path, dest_path, vols_path = temp_dirs

    create_vols_file(vols_path, "1")

    with pytest.raises(ValueError) as excinfo:
        run(src_path, dest_path, vols_path, "test")
    
    assert not os.path.isdir(dest_path)

def test_merge_bad_vols(temp_dirs):
    src_path, dest_path, vols_path = temp_dirs

    with pytest.raises(FileNotFoundError) as excinfo:
        run(src_path, dest_path, vols_path, "test")

def test_merge_vols_empty(temp_dirs):
    src_path, dest_path, vols_path = temp_dirs

    create_vols_file(vols_path, "")
    
    with pytest.raises(ValueError) as excinfo:
        run(src_path, dest_path, vols_path, "test")

def test_merge_vols_no_increasing(temp_dirs):
    src_path, dest_path, vols_path = temp_dirs

    create_vols_file(vols_path, "1, 3, 2")
    
    with pytest.raises(ValueError) as excinfo:
        run(src_path, dest_path, vols_path, "test")

def test_merge_missing_chapter(temp_dirs):
    src_path, dest_path, vols_path = temp_dirs

    create_vols_file(vols_path, "2")
    create_pdf(src_path, "ch 01.pdf")

    with pytest.raises(ValueError) as excinfo:
        run(src_path, dest_path, vols_path, "test")

def test_merge_duplicate_chapters(temp_dirs):
    src_path, dest_path, vols_path = temp_dirs

    create_vols_file(vols_path, "2")
    create_pdf(src_path, "ch 01.pdf")
    create_pdf(src_path, "ch 01.pdf")

    with pytest.raises(ValueError) as excinfo:
        run(src_path, dest_path, vols_path, "test")

def test_merge_corrupt_pdf(temp_dirs):
    src_path, dest_path, vols_path = temp_dirs

    create_vols_file(vols_path, "1")
    create_corrupt_pdf(src_path, "ch 01.pdf")

    with pytest.raises(Exception) as excinfo:
        run(src_path, dest_path, vols_path, "test")

def test_merge_valid_all(temp_dirs):
    src_path, dest_path, vols_path = temp_dirs

    create_vols_file(vols_path, "2, 5")

    for i in range(6):
        create_pdf(src_path, f"chapter {i}.pdf")
    
    run(src_path, dest_path, vols_path, "MyTest")

    assert os.path.isdir(dest_path)

    files = sorted(os.listdir(dest_path))
    assert len(files) == 2

    assert "MyTest Volume 1.pdf" in files[0]
    assert "MyTest Volume 2.pdf" in files[1]

    for f in files:
        assert os.path.getsize(os.path.join(dest_path, f)) > 0