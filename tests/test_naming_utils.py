import pytest

from src.utils.naming_utils import (
    create_chapter_name,
    create_volume_name,
    extract_chapter_number,
    extract_page_number,
    extract_volume_number
)


def test_create_chapter_name():
    assert create_chapter_name("Gyo", 3) == "Gyo Chapter 3"


def test_create_volume_name():
    assert create_volume_name("Gyo", 2) == "Gyo Volume 2"



# ------------------------------- extract volume --------------------------------------

@pytest.mark.parametrize(
    "name,expected",
    [
        ("Manga v01", 1), 
        ("Manga vol .01", 1), 
        ("Manga Vol.50", 50), 
        ("Manga volume.100", 100),
        ("Manga vol01", 1),
        ("Manga V 12dsa", 12),
        ("Manga v02sss", 2),
        ("Manga v03 001", 3),
        ("Manga v04 0101", 4)
    ],
)
def test_extract_volume_number_defaults(name, expected):
    assert extract_volume_number(name) == expected

def test_extract_volume_number_missing():
    with pytest.raises(ValueError, match="No volume number"):
        extract_volume_number("no_numbers_here.pdf")

def test_extract_volume_number_disallows_decimal():
    with pytest.raises(ValueError, match="No volume number"):
        extract_volume_number("Manga v2.5")



# --------------------------------- extract chapter ------------------------------------

@pytest.mark.parametrize(
    "name,expected",
    [
        ("Chapter 1", 1),
        ("ch. 12 stuff", 12),
        ("folder c 5 end", 5),
        ("MY CHAPTER 2.X", 2),
        ("prefix Chapter 3.5", 3.5),
        ("Manga Ch.150 [Group Name].cbz", 150),
        ("[Group] Manga c004v2.png", 4),
        ("Vol.02 Ch.45.5_clean.zip", 45.5),
        ("Chapter 99 - Extra Story.pdf", 99), 
        ("13DL.me-Chapter 10.png", 10),
    ],
)
def test_extract_chapter_number_defaults(name, expected):
    assert extract_chapter_number(name) == expected

def test_extract_chapter_number_missing():
    with pytest.raises(ValueError, match="No chapter number"):
        extract_chapter_number("no_numbers_here.pdf")

def test_extract_chapter_number_disallows_decimal():
    with pytest.raises(ValueError, match="Decimal chapter"):
        extract_chapter_number("Chapter 2.5", allow_decimal=False)

def test_extract_chapter_number_disallows_decimal_hidden():
    with pytest.raises(ValueError, match="Decimal chapter"):
        extract_chapter_number("ch 12.75", allow_decimal=False)



# ------------------------------ extract page --------------------------------------------

@pytest.mark.parametrize(
    "fname,expected",
    [
        ("page 001.png", 1),
        ("001.jpg", 1),
        ("Manga v02 000.png", 0),
        ("13DL.me-003.png", 3),
        ("13DL.me-004v.png", 4),
        ("Manga Vol. 01 (2005) (Digital TPB) (DarkZone-Empire) 006.jpeg", 6),
        ("Manga 5 00006.jpeg", 6),
        ("Manga 5 006.jpeg", 6),
        ("Manga 005 6fsa.jpeg", 6),
        ("__002.jpeg", 2),
        ("0002.jpeg", 2)
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
