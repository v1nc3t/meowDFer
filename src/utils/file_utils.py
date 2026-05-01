import os

def get_zip_files(src):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory not found: {src}")

    files = [f for f in os.listdir(src) if f.endswith(".zip")]
    
    if not files:
        raise ValueError(f"No files found in directory: {src}")

    return files