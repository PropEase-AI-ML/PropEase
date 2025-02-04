import os
import shutil

def save_uploaded_file(uploaded_file, upload_dir="uploads"):
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)
    
    return file_path

def read_file_content(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()
