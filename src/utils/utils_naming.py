import re

def extract_chapter_number(file_name):
    
    title_pattern = r'(?i)\b(?:chapter|ch\.?|c)\s*(\d+(?:\.\d)?)\b'

    match = re.search(title_pattern, file_name)

    return float(match.group(1)) if match else float('inf')

def extract_page_number(file_name):

    page_pattern = r'(\d+)'

    match = re.search(page_pattern, file_name)

    return float(match.group(1)) if match else float('inf')