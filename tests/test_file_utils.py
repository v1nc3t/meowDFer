import pytest

from meowdfer.utils import file_utils


def test_get_compressed_files_missing_dir(tmp_path):
    missing = tmp_path / "nope"
    with pytest.raises(FileNotFoundError, match="Source directory not found"):
        file_utils.get_compressed_files(str(missing))


def test_get_compressed_files_empty_dir(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    with pytest.raises(ValueError, match="No supported compressed files"):
        file_utils.get_compressed_files(str(d))
        

def test_get_folders_not_dir(tmp_path):
    f = tmp_path / "file"
    f.write_text("x")
    with pytest.raises(FileNotFoundError):
        file_utils.get_folders(str(f))


def test_get_folders_empty(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    with pytest.raises(ValueError, match="No folders"):
        file_utils.get_folders(str(d))


def test_get_folders_lists_directories(tmp_path):
    d = tmp_path / "root"
    d.mkdir()
    (d / "sub").mkdir()
    (d / "note.txt").write_text("hi")
    assert file_utils.get_folders(str(d)) == ["sub"]


def test_sort_chapters_orders_by_number():
    names = ["Chapter 10", "Chapter 2", "Chapter 1"]
    assert file_utils.sort_chapters(names, False) == ["Chapter 1", "Chapter 2", "Chapter 10"]

def test_sort_chapters_orders_by_number_decimal():
    names = ["Chapter 10.5", "Chapter 10.3", "Chapter 1"]
    assert file_utils.sort_chapters(names, True) == ["Chapter 1", "Chapter 10.3", "Chapter 10.5"]


def test_sort_chapters_empty_raises():
    with pytest.raises(ValueError, match="No folders found to sort"):
        file_utils.sort_chapters([], False)


def test_get_images_filters_extensions(tmp_path):
    d = tmp_path / "img"
    d.mkdir()
    (d / "a.png").touch()
    (d / "b.jpg").touch()
    (d / "c.jpeg").touch()
    (d / "d.gif").touch()
    names = sorted(file_utils.get_images(str(d)))
    assert names == ["a.png", "b.jpg", "c.jpeg"]


def test_get_images_none_raises(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    with pytest.raises(ValueError, match="No images"):
        file_utils.get_images(str(d))


def test_sort_page_number_orders_numerically(tmp_path):
    files = ["page 10.png", "page 2.png", "page 01.png"]
    assert file_utils.sort_page_number(files) == ["page 01.png", "page 2.png", "page 10.png"]


def test_sort_page_number_empty_raises():
    with pytest.raises(ValueError, match="No files found"):
        file_utils.sort_page_number([])


def test_get_pdfs_case_insensitive(tmp_path):
    d = tmp_path / "p"
    d.mkdir()
    (d / "a.PDF").touch()
    (d / "b.pdf").touch()
    names = sorted(file_utils.get_pdfs(str(d)))
    assert names == ["a.PDF", "b.pdf"]


def test_get_pdfs_none_raises(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    with pytest.raises(ValueError, match="No PDF"):
        file_utils.get_pdfs(str(d))


def test_get_volumes_file_reads_intervals(tmp_path):
    p = tmp_path / "vols.txt"
    p.write_text("5, 10, 15")
    assert file_utils.get_volumes_file(str(p)) == [5, 10, 15]


def test_get_volumes_file_multiline_normalized(tmp_path):
    p = tmp_path / "vols.txt"
    p.write_text("2,\n3,\n4")
    assert file_utils.get_volumes_file(str(p)) == [2, 3, 4]


def test_get_volumes_file_missing():
    with pytest.raises(FileNotFoundError):
        file_utils.get_volumes_file("/no/such/vols.txt")


def test_get_volumes_file_empty_raises(tmp_path):
    p = tmp_path / "vols.txt"
    p.write_text("  ,  ,\n")
    with pytest.raises(ValueError, match="non-empty"):
        file_utils.get_volumes_file(str(p))


def test_get_volumes_file_must_be_sorted(tmp_path):
    p = tmp_path / "vols.txt"
    p.write_text("10, 5")
    with pytest.raises(ValueError, match="strictly increasing"):
        file_utils.get_volumes_file(str(p))


def test_get_chapter_map_unique_keys():
    files = ["Chapter 1.pdf", "Ch 2.pdf"]
    m = file_utils.get_chapter_map(files, False)
    assert m == {1: "Chapter 1.pdf", 2: "Ch 2.pdf"}
    
def test_get_chapter_map_decimal_keys():
    files = ["Chapter 1.3.pdf", "Ch 1.pdf", "c 2.pdf"]
    m = file_utils.get_chapter_map(files, True)
    assert m == {1: "Ch 1.pdf", 1.3: "Chapter 1.3.pdf", 2: "c 2.pdf"}


def test_get_chapter_map_duplicate_raises():
    with pytest.raises(ValueError, match="Duplicate chapter"):
        file_utils.get_chapter_map(["Chapter 1 a.pdf", "Chapter 1 b.pdf"], False)
