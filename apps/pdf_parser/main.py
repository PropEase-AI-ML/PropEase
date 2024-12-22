# receives a PDF file and outputs a folder containing parsed texts
import argparse
import logging
import os
from typing import List

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse

logger = logging.getLogger(__name__)

load_dotenv(override=True)

LLAMA_PARSE_API_KEY = os.getenv("LLAMA_PARSE_API_KEY")

def loop_pdf_files(folder_path: str) -> List[str]:
    """
    Loops over PDF files in the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing PDF files
    
    Returns:
        List[str]: List of full paths to PDF files in the folder
    """
    # List to store PDF file paths
    pdf_files = []
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return pdf_files
    
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a PDF
        if filename.lower().endswith('.pdf'):
            # Create full file path
            full_path = os.path.join(folder_path, filename)
            pdf_files.append(full_path)
            print(f"Found PDF: {filename}")
    
    return pdf_files

def parse(filepath: str):
    """
    Parses the text from a PDF file.
    
    Args:
        pdf_file (str): Path to the PDF file to parse
    
    Returns:
        str: Parsed text from the PDF
    """
    logger.info(f"Parsing PDF file: {filepath}")
    # Set up parser
    parser = LlamaParse(
        api_key=LLAMA_PARSE_API_KEY,
        result_type="text", # "markdown" and "text" are available
        max_pages=5,
        disable_ocr=True,
        disable_image_extraction=True,
    )

    file_extractor = {".pdf": parser}
    
    return SimpleDirectoryReader(input_files=[f'{filepath}'], file_extractor=file_extractor).load_data()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Loop through PDF files in a folder.')
    
    # Add folder path argument
    parser.add_argument('--folder_path',
                        '-fp', 
                        type=str, 
                        required=True, 
                        help='Path to the folder containing PDF files')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Get list of PDF files in the folder
    pdf_files = loop_pdf_files(args.folder_path)
    
    # Parse each PDF file
    for pdf_file in pdf_files:
        documents = parse(pdf_file)
        # Save parsed text to a file
        for doc in documents:
            with open(f"{pdf_file.split('.')[0]}.txt", "a") as f:
                f.write(doc.text)