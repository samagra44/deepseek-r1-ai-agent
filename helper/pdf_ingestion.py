import tempfile
import streamlit as st
from datetime import datetime
from langchain_community.document_loaders import PyMuPDFLoader

def process_pdf(upload_file):
    """Extract and process the text from PDF"""
    try:
        with tempfile.NamedTemporaryFile(delete=False,  suffix=".pdf") as temp:
            temp.write(upload_file.read())
            loader = PyMuPDFLoader(temp.name)
            documents = loader.load()
        
        for doc in documents:
            doc.metadata.update({
                "source_type": "pdf",
                "file_name": upload_file.name,
                "timestamp": datetime.now().isoformat()
            })
        return documents
    except Exception as e:
        #print(e)
        st.error(f"Error processing PDF: {e}")
        return []