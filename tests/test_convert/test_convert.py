import os
import io
import pytest

from PIL import Image
from src.commands.convert.convert_pdf import run

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

@pytest.fixture
def temp_dirs(tmp_path):
    src = tmp_path / "src"
    dest = tmp_path / "dest"
    src.mkdir()
    return str(src), str(dest)

def create_folder(src_path, name):
    folder_path = os.path.join(src_path, name)
    os.makedirs(folder_path, exist_ok=True)

    return folder_path

def create_img(src_path, num):
    img_name = f'{num}.png'
    img_path = os.path.join(src_path, img_name)

    img = Image.new('RGB', (100, 100), color='red')
    img.save(img_path)

def create_junk_img(src_path, num):
    img_name = f'{num}.png'
    img_path = os.path.join(src_path, img_name)
    
    with open(img_path, 'wb') as f:
        f.write(os.urandom(1024))

def create_truncated_img(src_path, num):
    img_name = f'{num}.png'
    img_path = os.path.join(src_path, img_name)

    buf = io.BytesIO()
    img = Image.new('RGB', (100, 100), color='red')
    img.save(buf, format='PNG')
    
    broken_data = buf.getvalue()[:50]

    with open(img_path, 'wb') as f:
        f.write(broken_data)
    
def create_imposter_img(src_path, num):
    img_name = f'{num}.png'
    img_path = os.path.join(src_path, img_name)
    
    with open(img_path, 'w') as f:
        f.write("This is txt file, not img")

# --- tests ---

def test_convert_bad_source(temp_dirs):
    src_path, dest_path = temp_dirs

    with pytest.raises(FileNotFoundError) as excinfo:
        run("src_bad", dest_path, "test")
    
    assert not os.path.isdir(dest_path)

def test_convert_empty(temp_dirs):
    src_path, dest_path = temp_dirs

    with pytest.raises(ValueError) as excinfo:
        run(src_path, dest_path, "test")

def test_convert_folder_bad_name(temp_dirs):
    src_path, dest_path = temp_dirs

    folder_path1 = create_folder(src_path, 'nochapter 1')
    folder_path2 = create_folder(src_path, 'chapter')
    folder_path3 = create_folder(src_path, '1')

    with pytest.raises(ValueError) as excinfo:
        run(src_path, dest_path, "test")

def test_convert_img_bad_name(temp_dirs):
    src_path, dest_path = temp_dirs

    folder_path = create_folder(src_path, 'c 1')
    create_img(folder_path, 'no_number')

    with pytest.raises(ValueError) as excinfo:
        run(src_path, dest_path, "test")

def test_convert_folder_empty(temp_dirs):
    src_path, dest_path = temp_dirs

    folder_path = create_folder(src_path, 'c 1')

    with pytest.raises(ValueError) as excinfo:
        run(src_path, dest_path, "test")

def test_convert_junk_img(temp_dirs):
    src_path, dest_path = temp_dirs

    folder_path = create_folder(src_path, 'c 1')
    create_junk_img(folder_path, '1')

    with pytest.raises(RuntimeError) as excinfo:
        run(src_path, dest_path, "test")
        
def test_convert_truncated_img(temp_dirs):
    src_path, dest_path = temp_dirs

    folder_path = create_folder(src_path, 'c 1')
    create_truncated_img(folder_path, '1')

    with pytest.raises(OSError) as excinfo:
        run(src_path, dest_path, "test")
        
def test_convert_imposter_img(temp_dirs):
    src_path, dest_path = temp_dirs

    folder_path = create_folder(src_path, 'c 1')
    create_imposter_img(folder_path, '1')

    with pytest.raises(RuntimeError) as excinfo:
        run(src_path, dest_path, "test")

def test_convert_valid_all(temp_dirs):
    src_path, dest_path = temp_dirs

    folder_path = create_folder(src_path, 'c 1')
    create_img(folder_path, '1')
    create_img(folder_path, '2')
    create_img(folder_path, '3')

    run(src_path, dest_path, 'test')

    assert os.path.isdir(dest_path)

    files = os.listdir(dest_path)
    assert len(files) == 1

    expected = 'test Chapter 1.pdf'
    assert expected in files

    pdf_path = os.path.join(dest_path, expected)
    assert os.path.isfile(pdf_path)
    assert os.path.getsize(pdf_path) > 0