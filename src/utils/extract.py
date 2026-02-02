import os

from zipfile import ZipFile, BadZipFile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def extract_zips(src, dest):
    # Extract all .zip files from the src into dest

    src = os.path.join(PROJECT_ROOT, src)
    dest = os.path.join(PROJECT_ROOT, dest)

    try:
        os.makedirs(dest, exist_ok=True)

        for file_name in os.listdir(src):
            if file_name.endswith(".zip"):
                zip_path = os.path.join(src, file_name)
                try:
                    with ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(dest)
                        print(f"Extracted: {file_name}")
                except BadZipFile:
                    print(f"Invalid zip file: {file_name}")
                except Exception as e:
                    print(f"Failed to extract {file_name}: {e}")
        
        print(f"\nExtracted all zips")
    except FileNotFoundError:
        print(f"Source directory not found: {src}")
    except PermissionError:
        print(f"Permission denied.")
    except Exception as e:
        print(f"Unexpected error: {e}")