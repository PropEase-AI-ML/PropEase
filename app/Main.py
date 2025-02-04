import streamlit as st
from utils.preprocess import preprocess
from utils.date_extraction_small import extract_expiry_dates
from utils.file_utils import save_uploaded_file, read_file_content
from utils.pytesseract_extract import pytesseract_api_call
import joblib
import json
import requests

from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

# Load Model
model = joblib.load(os.getenv("MODEL_PATH"))
vectorizer = joblib.load(os.getenv("VECTORIZER_PATH"))

def lr_predict(doc_text):
    # Predict probabilities
    probabilities = model.predict_proba(doc_text)

    # Set confidence threshold
    threshold = 0.62

    predictions = []
    for prob in probabilities:
        max_prob = np.max(prob)
        if max_prob < threshold:
            predictions.append("Other")  # Low confidence → classify as Other
        else:
            predictions.append(model.classes_[np.argmax(prob)])  # Class A or B

    return predictions

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

headers = {
    'accept': 'application/json',
}

if uploaded_file:
    
    # with st.spinner("Processing..."):
    #     try:
    #         files = {
    #             'file': (uploaded_file.name, uploaded_file, 'application/pdf')
    #         }
            
    #         # Send file to the FastAPI backend
    #         response = requests.post(f"{BACKEND_URL}/api/v1/documents/upload", headers=headers, files=files)

    #         if response.status_code == 200:
    #             result = response.json()
    #             st.success("PDF processed successfully!")
    #         else:
    #             st.error(f"Failed to process PDF: {response.status_code}")
    #     except Exception as e:
    #         st.error(f"Error: {e}")
    
    file_path = save_uploaded_file(uploaded_file)

    with st.status("Processing... Please wait", expanded=True) as status:
        result, extracted_file_path = pytesseract_api_call(uploaded_file.name)
        status.update(label="✅ File processed successfully!", state="complete", expanded=False)

        document_content = read_file_content(extracted_file_path)

        processed_doc = preprocess(document_content)
        doc_vectorized = vectorizer.transform([processed_doc])
        prediction = lr_predict(doc_vectorized)[0]
        if prediction == "Other":
            expiring_date = "None"
        else:
            expiring_date = extract_expiry_dates(document_content)

        with open(f'preds/{uploaded_file.name.replace(".pdf", ".json")}', "w") as json_file:
            json.dump({'report_type': prediction, 'expiring_date': str(expiring_date)}, json_file, indent=4)

    st.success("File uploaded successfully! Go to the pages to view the document.")
