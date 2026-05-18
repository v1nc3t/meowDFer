import re
import os

VOLUME_RX = re.compile(r'(?i)(?:^|[-_\s])(?:volume|vol\.?|v)\s*(\d+)')
PAGE_RX = re.compile(r'(\d+)[^\d]*$')

def extract_volume_number(file_name: str) -> int:
    base_name = os.path.basename(file_name)
    match = VOLUME_RX.search(base_name)
    
    if not match:
        raise ValueError(f"No volume number found in: {file_name}")
    
    return int(match.group(1))


def create_volume_name(name: str, volume_number: int) -> str:
    return f"{name} Volume {volume_number}"


def create_chapter_name(name: str, chapter_number: int) -> str:
    return f"{name} Chapter {chapter_number}"


def extract_chapter_number(file_name: str, allow_decimal: bool = True) -> float:
    base_name = os.path.basename(file_name)
    
    clean_name = re.sub(r'(?i)\b\d+DL\.me[-_]?|(?:\w+\.)+\w+[-_]?', '', base_name)
    
    digit_pattern = r'\d+(?:\.\d+)?' if allow_decimal else r'\d+'
    
    pattern = rf'(?i)(?:^|[-_\s])(?:chapter|ch\.?)\s*({digit_pattern})(?=[a-z]?\b)|(?:^|[-_\s])c({digit_pattern})(?=[a-z]?\b)|(?:^|[-_\s])({digit_pattern})(?=[a-z]?\b)?$'
    
    match = re.search(pattern, clean_name.strip())

    if not match:
        raise ValueError(f"No chapter number found in: {file_name}")
        
    number_str = match.group(1) or match.group(2) or match.group(3)

    num = float(number_str)
    
    return int(num) if num.is_integer() else num


def extract_page_number(file_name: str) -> int:
    base_name = os.path.basename(file_name)
    match = PAGE_RX.search(base_name)

    if not match:
        raise ValueError(f"No page number found in: {file_name}")
    
    return int(match.group(1))
