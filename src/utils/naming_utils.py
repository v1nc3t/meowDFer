import re
import os

VOLUME_RX = re.compile(r'(?i)(?:^|[-_\s])(?:volume|vol|v)[\s.]*(\d+)(?!\.\d)')
CHAPTER_PREFIX_RX = re.compile(
    r'(?i)(?:(?:^|[-_\s])(?:chapter|ch\.?|c)\s*|(?<=^)|(?<=[-\s_]))(\d+(?:\.\d+)?)'
)
PAGE_RX = re.compile(r'(?<!\.)(\d+)[^\d]*?\.[a-zA-Z0-9]+$')


def create_volume_name(name: str, volume_number: float) -> str:
    return f"{name} Volume {volume_number}"

def extract_volume_number(file_name: str) -> int:
    base_name = os.path.basename(file_name)
    match = VOLUME_RX.search(base_name)
    
    if not match:
        raise ValueError(f"No volume number found in: {file_name}")
    
    return int(match.group(1))


def create_chapter_name(name: str, chapter_number: float) -> str:
    return f"{name} Chapter {chapter_number}"

def extract_chapter_number(file_name: str, allow_decimal: bool = True) -> float:
    base_name = os.path.basename(file_name)
    
    clean_name = re.sub(r'(?i)\b\d+DL\.me[-_]?', '', base_name)
    
    match = CHAPTER_PREFIX_RX.search(clean_name)
    if not match:
        raise ValueError(f"No chapter number found in: {file_name}")
        
    raw_num = match.group(1)
    
    if not allow_decimal and '.' in raw_num:
        raise ValueError(f"Decimal chapter numbers are not allowed: {file_name}")
        
    num = float(raw_num)
    return int(num) if num.is_integer() else num


def extract_page_number(file_name: str) -> int:
    base_name = os.path.basename(file_name)
    match = PAGE_RX.search(base_name)

    if not match:
        if re.search(r'\d+\.\d+', base_name):
            raise ValueError(f"Decimal page numbers are not allowed in: {file_name}")
        raise ValueError(f"No page number found in: {file_name}")
    
    return int(match.group(1))
