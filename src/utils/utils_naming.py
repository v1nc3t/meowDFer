import re

def create_chapter_name(name, chapter_number):
    return f"{name} Chapter {chapter_number}"

def extract_chapter_number(file_name):
    match = re.search(
        r'(?i)\b(?:chapter|ch\.?|c)\s*(\d+(?:\.\d+)?)\b',
        file_name
    )

    if not match:
        raise ValueError(f"No chapter number found")
    
    number_str = match.group(1)
    if '.' in number_str:
        raise ValueError(f"Decimal chapter number are skipped")

    return int(number_str)

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
