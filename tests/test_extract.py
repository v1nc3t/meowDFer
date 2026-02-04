import os
import pytest

from zipfile import ZipFile, BadZipFile
from meowDFer.utils import extract as test

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@pytest.fixture
def tmp_dirs(tmp_path):
    zips = tmp_path / "zips"
    out = tmp_path / "out"
    
    zips.mkdir()
    return zips, out

def test_extract_one_zip(tmp_dirs):
    zips, out = tmp_dirs

    zip_path = zips / "test.zip"

    with ZipFile(zip_path, "w") as z:
        z.writestr("file.txt", "test")

    test.extract_zips(str(zips), str(out))

    assert out.exists()
    assert (out / "file.txt").exists()
    assert (out / "file.txt").read_text() == "test"

def test_extract_many_zips(tmp_dirs):
    zips, out = tmp_dirs

    zip_path = zips / "test.zip"

    with ZipFile(zip_path, "w") as z:
        z.writestr("file1.txt", "test1")
        z.writestr("file2.txt", "test2")

    test.extract_zips(str(zips), str(out))

    assert out.exists()
    assert (out / "file1.txt").exists()
    assert (out / "file1.txt").read_text() == "test1"
    assert (out / "file2.txt").exists()
    assert (out / "file2.txt").read_text() == "test2"



def test_extract_bad_zip(tmp_dirs):
    zips, out = tmp_dirs

    bad_zip = zips / "test.zip"
    bad_zip.write_text("this is not a zip")

    test.extract_zips(str(zips), str(out))

    assert out.exists()
    assert list(out.iterdir()) == []



def test_extract_mixed_zips(tmp_dirs):
    zips, out = tmp_dirs

    good = zips / "good.zip"
    with ZipFile(good, "w") as z:
        z.writestr("ok.txt", "good")

    bad = zips / "bad.zip"
    bad.write_text("bad zip file")

    test.extract_zips(str(zips), str(out))

    assert (out / "ok.txt").exists()
    assert (out / "ok.txt").read_text() == "good"

