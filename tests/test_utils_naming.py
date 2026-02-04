import pytest

from src.utils import utils_naming as test


def test_extract_chapter_integer():
    assert test.extract_chapter_number("Chapter 10") == 10, "chapter integer"
    assert test.extract_chapter_number("Ch.10") == 10, "ch. integer"
    assert test.extract_chapter_number("c001") == 1, "c integer"

def test_extract_no_chapter():
    with pytest.raises(ValueError) as excinfo:
        test.extract_chapter_number("test 1")

    assert "No chapter number found" in str(excinfo.value)
 
def test_extract_chapter_decimal():
    with pytest.raises(ValueError) as excinfo:
        test.extract_chapter_number("chapter 1.5")
    
    assert "Decimal chapter number are skipped" in str(excinfo)

def test_extract_page_integer():
    assert test.extract_page_number("page 9.jpeg") == 9

def test_extract_page_decimal():
    with pytest.raises(ValueError) as excinfo:
        test.extract_page_number("page 2.5")
    
    assert "Decimal page number not allowed" in str(excinfo)

def test_extract_page_no_number():
    with pytest.raises(ValueError) as excinfo:
        test.extract_page_number("page")
    
    assert "No page number found" in str(excinfo)


def test_create_chapter_name():
    assert test.create_chapter_name("Test", 1) in "Test Chapter 1"