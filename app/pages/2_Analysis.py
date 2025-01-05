import streamlit as st
import os
import json

from utils.file_utils import read_file_content

st.markdown("# Document Analysis 🎉")
st.markdown(
    """
    ### Document Analysis Section
    Analyze the content of your uploaded documents. This section provides:
    - **Extracted Text** – Shows the plain text and layout extracted from the LLM-/OCR-based models.
    - **Metadata** – Displays the classification and expire date of the chosen document.
    
    Use this feature to gain insights into document structure and identify key terms.
    """
)

uploaded_files = os.listdir("uploads")
if uploaded_files:
    selected_file = st.selectbox("Select a file to analyze", uploaded_files)
    file_path = os.path.join("extracted", selected_file.split('.')[0] + '.txt')

    with open(os.path.join("preds", selected_file.split('.')[0] + '.json')) as json_file:
        preds = json.load(json_file)
    
    st.write("Predicted Metadata")
    st.code(preds, language="json")

    document_content = read_file_content(file_path)
    st.text_area("Raw Document", document_content, height=700)

else:
    st.warning("No files uploaded yet. Please upload from the main page.")
