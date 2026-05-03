import pytest

from src.utils.naming_utils import (
    create_chapter_name,
    create_volume_name,
    extract_chapter_number,
    extract_page_number,
)


def test_create_chapter_name():
    assert create_chapter_name("Gyo", 3) == "Gyo Chapter 3"


def test_create_volume_name():
    assert create_volume_name("Gyo", 2) == "Gyo Volume 2"


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Chapter 1", 1),
        ("ch. 12 stuff", 12),
        ("folder c 5 end", 5),
        ("MY CHAPTER 2.X", 2),
        ("prefix Chapter 3.5 suffix", 3.5),
    ],
)
def test_extract_chapter_number_defaults(name, expected):
    assert extract_chapter_number(name) == expected


def test_extract_chapter_number_case_insensitive():
    assert extract_chapter_number("CHAPTER 9") == 9


def test_extract_chapter_number_missing():
    with pytest.raises(ValueError, match="No chapter number"):
        extract_chapter_number("no_numbers_here.pdf")


def test_extract_chapter_number_disallows_decimal():
    with pytest.raises(ValueError, match="Decimal chapter"):
        extract_chapter_number("Chapter 2.5", allow_decimal=False)


@pytest.mark.parametrize(
    "fname,expected",
    [
        ("page 001.png", 1),
        ("001.jpg", 1),
        ("scan_12_final.png", 12),
    ],
)
def test_extract_page_number(fname, expected):
    assert extract_page_number(fname) == expected


def test_extract_page_number_rejects_decimal():
    with pytest.raises(ValueError, match="Decimal page"):
        extract_page_number("img 2.5.png")


def test_extract_page_number_missing_digit():
    with pytest.raises(ValueError, match="No page number"):
        extract_page_number("no_digits_here")
