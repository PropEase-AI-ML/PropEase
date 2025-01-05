import streamlit as st
import os
from streamlit_pdf_viewer import pdf_viewer
from utils.file_utils import read_file_content

import dotenv

dotenv.load_dotenv(override=True)

if 'pages' not in st.session_state:
    st.session_state['pages'] = None

if 'page_selection' not in st.session_state:
    st.session_state['page_selection'] = []


st.markdown("# Raw Document Viewer ❄️")
st.markdown(
    """
    ### Document Viewing Section
    In this section, you can view the raw content of uploaded documents. 
    Select the file from the dropdown to display its contents.
    
    This feature is useful for inspecting document structure and verifying upload success.
    """
)

with st.sidebar:

    st.subheader("Height and width")
    width = st.slider(label="PDF width", min_value=100, max_value=1000, value=700)
    height = st.slider(label="PDF height", min_value=-1, max_value=10000, value=800)

uploaded_files = os.listdir("uploads")
if uploaded_files:
    selected_file = st.selectbox("Select a file to view", uploaded_files)
    file_path = os.path.join("uploads", selected_file)
    
    if selected_file.endswith(".pdf"):
        with open(file_path, "rb") as f:
            pdf_data = f.read()
        
        pdf_viewer(input=pdf_data, width=width, height=height)

    else:
        # Initialize document_content outside the try block
        document_content = read_file_content(file_path)
        st.text_area("Raw Document", document_content, height=700)
else:
    st.warning("No files uploaded yet. Please upload from the main page.")