import os

def save_uploaded_file(uploaded_file):
    file_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            return f.read()
