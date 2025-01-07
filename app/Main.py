import streamlit as st
from utils.preprocess import preprocess
from utils.date_extraction import extract_dates
from utils.file_utils import save_uploaded_file, read_file_content
from utils.pytesseract_extract import pytesseract_api_call
import joblib
import json

from dotenv import load_dotenv
import os

load_dotenv()

# Load Model
model = joblib.load(os.getenv("MODEL_PATH"))
vectorizer = joblib.load(os.getenv("VECTORIZER_PATH"))

os.makedirs("preds", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("extracted", exist_ok=True)

st.markdown("# Main page 🎈")
st.markdown("""
    Welcome to the **PropEase**. 

    This application allows you to upload text or PDF files for processing and analysis.
    Use the navigation bar on the left to switch between different sections of the app.

    ### Upload Section
    Use the uploader below to add your document to the app. Supported formats include:
    - **PDF** (Portable Document Format)
    
    Once uploaded, you can view or analyze your document by navigating to the respective sections.
""")

uploaded_file = st.file_uploader("Upload a Document", type=["pdf"])

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)

    with st.status("Processing... Please wait", expanded=True) as status:
        result, extracted_file_path = pytesseract_api_call(uploaded_file.name)
        status.update(label="✅ File processed successfully!", state="complete", expanded=False)

        document_content = read_file_content(extracted_file_path)

        processed_doc = preprocess(document_content)
        doc_vectorized = vectorizer.transform([processed_doc])
        prediction = model.predict(doc_vectorized)[0]
        expiring_date = extract_dates(document_content)

        with open(f'preds/{uploaded_file.name.replace(".pdf", ".json")}', "w") as json_file:
            json.dump({'report_type': prediction, 'expiring_date': expiring_date}, json_file, indent=4)

    st.success("File uploaded successfully! Go to the pages to view the document.")
