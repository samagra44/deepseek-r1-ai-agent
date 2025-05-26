import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from datetime import datetime

def process_web(url: str):
    """Extract and process text from a web page"""
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        for doc in documents:
            doc.metadata.update({
                "source": url,
                "timestamp": datetime.now().isoformat()
            })
        return documents
    except Exception as e:
        #print(e)
        st.error(f"Error processing URL: {e}")
        return []