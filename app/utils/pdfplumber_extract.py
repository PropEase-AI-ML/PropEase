import os
import pdfplumber

def pdfplumber_api_call(selected_file, max_pages=5):
   
    init_page = 0
    with pdfplumber.open(os.path.join("uploads", selected_file)) as pdf:

        ocr_text = ""

        for page_num in range(max_pages):
            cur_page = pdf.pages[page_num]
            ocr_text += f"\n\n--- Page {page_num + 1} ---\n{cur_page.extract_text()}"
            
        with open(f"{os.path.join('data/test', selected_file.split('.')[0])}.txt", "w") as f:
            f.write(ocr_text)