from pdf2image import convert_from_path
import pytesseract
from pytesseract import Output

import os

def pytesseract_api_call(selected_file, max_pages=5):

    pdf_path = os.path.join(os.path.join("uploads", selected_file))
    # Convert PDF to a list of images (one per page)
    pages = convert_from_path(pdf_path, dpi=300)  # 300 DPI for better OCR accuracy

    # Perform OCR on each page
    for page_num, page in enumerate(pages):
        # Perform OCR
        if page_num < max_pages:
            d = pytesseract.image_to_data(page, lang='fra+nld', output_type=Output.DICT)

    ocr_text = ""

    for page_num, page in enumerate(pages):
        if page_num < max_pages:
            text = pytesseract.image_to_string(page, lang='fra+nld')
            ocr_text += f"\n\n--- Page {page_num + 1} ---\n{text}"

    os.makedirs("extracted", exist_ok=True)
    extracted_file_path = f"{os.path.join('extracted', selected_file).replace('.pdf', '.txt')}" # pdf to txt

    with open(extracted_file_path, "w") as f:
        f.write(ocr_text)
    
    return f"Processing of {selected_file} completed!", extracted_file_path