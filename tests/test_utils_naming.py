import pytest

from src.utils import utils_naming


def test_extract_chapter_integer():
    assert utils_naming.extract_chapter_number("Chapter 10") == 10, "chapter integer"
    assert utils_naming.extract_chapter_number("Ch.10") == 10, "ch. integer"
    assert utils_naming.extract_chapter_number("c001") == 1, "c integer"

def test_extract_no_chapter():
    with pytest.raises(ValueError) as excinfo:
        utils_naming.extract_chapter_number("test 1")

    assert "No chapter number found" in str(excinfo.value)
 
def test_extract_chapter_decimal():
    assert utils_naming.extract_chapter_number("Chapter 9.5") == 9.5, "chapter decimal"
    assert utils_naming.extract_chapter_number("Ch. 9.5") == 9.5, "ch. decimal" 
    assert utils_naming.extract_chapter_number("c009.5") == 9.5, "c decimal"

def test_extract_page_integer():
    assert utils_naming.extract_page_number("page 9.jpeg") == 9

def test_create_chapter_name():
    assert utils_naming.create_chapter_name("Test", 1) == "Test Chapter 1"