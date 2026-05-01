import re

def create_chapter_name(name, chapter_number):
    return f"{name} Chapter {chapter_number}"

def create_volume_name(name, volume_number):
    return f"{name} Volume {volume_number}"

def extract_chapter_number(file_name, allow_decimal=True):
    match = re.search(
        r'(?i)\b(?:chapter|ch\.?|c)\s*(\d+(?:\.\d+)?)\b',
        file_name
    )

    if not match:
        raise ValueError(f"No chapter number found in: {file_name}")
    
    number_str = match.group(1)
    
    if '.' in number_str and not allow_decimal:
        raise ValueError(f"Decimal chapter: {number_str}")

    num = float(number_str)

    return int(num) if num.is_integer() else num

def extract_page_number(file_name):

    page_pattern = r'(\d+)'

    match = re.search(
        r'\d+(?:\.\d+)?',
        file_name
    )

    if not match:
        raise ValueError(f"No page number found")
    
    number_str = match.group()
    if '.' in number_str:
        raise ValueError("Decimal page number not allowed")
    
    return int(number_str)
