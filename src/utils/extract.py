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
                        print(f"\033[92mExtracted successfully: {file_name}\033[0m")
                except BadZipFile:
                    print(f"\033[91mInvalid zip file: {file_name}\033[0m")
                except Exception as e:
                    print(f"\033[91mFailed to extract {file_name}: {e}\033[0m")
        
        print(f"\n\033[95mExtracted all zips\033[0m\n")
    except FileNotFoundError:
        print(f"\033[91mSource directory not found: {src}\033[0m")
    except PermissionError:
        print(f"\033[91mPermission denied.\033[0m")
    except Exception as e:
        print(f"\033[91mUnexpected error: {e}\033[0m")