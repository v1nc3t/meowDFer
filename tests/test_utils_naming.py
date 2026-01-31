
from src.utils import utils_naming


def test_extract_chapter_integer():
    assert utils_naming.extract_chapter_number("Chapter 10") == 10

def test_extract_ch_integer():
    assert utils_naming.extract_chapter_number("Ch.10") == 10

def test_extract_c_integer():
    assert utils_naming.extract_chapter_number("C001") == 1

def test_extract_chapter_decimal():
    assert utils_naming.extract_chapter_number("Chapter 9.5") == 9.5

def test_extract_ch_decimal():
    assert utils_naming.extract_chapter_number("Ch. 9.5") == 9.5

def test_extract_c_decimal():
    assert utils_naming.extract_chapter_number("c002.5") == 2.5

def test_extract_page_integer():
    assert utils_naming.extract_page_number("9.jpeg") == 9

def test_extract_page_decimal():
    assert utils_naming.extract_page_number("9.5.jpeg") == 9