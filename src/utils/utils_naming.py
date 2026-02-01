import re

def create_chapter_name(name, chapter_number):
    return f"{name} Chapter {chapter_number}"

def extract_chapter_number(file_name):
    match = re.search(
        r'(?i)\b(?:chapter|ch\.?|c)\s*(\d+(?:\.\d+)?)\b',
        file_name
    )

    if not match:
        raise ValueError(f"No chapter number found in `{file_name}`")
        
    return float(match.group(1))

def extract_page_number(file_name):

    page_pattern = r'(\d+)'

    match = re.search(
        r'(\d+)(?=\D*$)',
        file_name
    )

    return float(match.group(1))
