import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
from agno.vectordb.chroma import ChromaDb
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import streamlit as st
# from config.node import GOOGLE_API_KEY
# from config.node import COLLECTION_NAME
# from config.node import GOOGLE_EMBEDDING_MODEL
# from config.node import HUGGINGFACE_EMBEDDING_MODEL
# from config.node import HUGGINGFACE_API_KEY
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

# os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
COLLECTION_NAME = st.secrets["COLLECTION_NAME"]
HUGGINGFACE_EMBEDDING_MODEL = st.secrets["HUGGINGFACE_EMBEDDING_MODEL"]
COLLECTION_NAME = COLLECTION_NAME

MODEL = HUGGINGFACE_EMBEDDING_MODEL

EMBEDDING_MODEL = HuggingFaceEndpointEmbeddings(
    model=MODEL,
    huggingfacehub_api_token=HUGGINGFACE_API_KEY,
)

# EMBEDDING_MODEL = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)

def init_chroma():
    """Initializes the ChromaDB instance."""
    chroma = ChromaDb(
        collection=COLLECTION_NAME,
        path="./chroma_db",
        embedder=EMBEDDING_MODEL,
        persistent_client=True
    )
    try:
        chroma.client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        chroma.create() 
    return chroma