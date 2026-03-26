import os
import pytest

from zipfile import ZipFile, BadZipFile
from src.commands.extract.extract_zips import run

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

@pytest.fixture
def temp_dirs(tmp_path):
    src = tmp_path / "src"
    dest = tmp_path / "dest"
    src.mkdir()
    return str(src), str(dest)

def create_good_zip(src_path, num):
    filename = f"good_{num}.zip"
    zip_path = os.path.join(src_path, filename)

    with ZipFile(zip_path, "w") as z:
        z.writestr(f"{num}.txt", str(num))
    
    return zip_path

def create_bad_zip(src_path, num):
    filename = f"bad_{num}.zip"
    zip_path = os.path.join(src_path, filename)

    with open(zip_path, "wb") as f:
        f.write(b"This is not a zip file.")

    return zip_path

# --- tests ---

def test_extract_empty(temp_dirs):
    src_path, dest_path = temp_dirs
    
    run(src_path, dest_path)

    assert not os.path.isdir(dest_path)

def test_extract_zips(temp_dirs):
    src_path, dest_path = temp_dirs

    create_good_zip(src_path, 1)
    create_good_zip(src_path, 2)

    run(src_path, dest_path)

    file1 = os.path.join(dest_path, "1.txt")
    file2 = os.path.join(dest_path, "2.txt")

    assert os.path.exists(file1)
    with open(file1, "r") as f:
        assert f.read() == "1"
    
    assert os.path.exists(file2)
    with open(file2, "r") as f:
        assert f.read() == "2"

def test_extract_bad_zips(temp_dirs):
    src_path, dest_path = temp_dirs

    create_bad_zip(src_path, 1)
    
    run(src_path, dest_path)

    assert not os.path.isdir(dest_path)

def test_extract_mixed_zips(temp_dirs):
    src_path, dest_path = temp_dirs

    create_good_zip(src_path, 1)
    create_bad_zip(src_path, 2)

    run(src_path, dest_path)

    extracted_file = os.path.join(dest_path, "hello.txt")

    assert not os.path.exists(extracted_file)
    assert not os.path.isdir(dest_path)