from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import UploadFile
from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    return [doc for doc in RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(documents) if doc.page_content.strip()]
async def read_pdf(upload, max_bytes):
    content = await upload.read(max_bytes + 1)
    if len(content) > max_bytes: raise ValueError("The uploaded file exceeds the configured size limit.")
    if not content: raise ValueError("The uploaded PDF is empty.")
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp: temp.write(content); path = Path(temp.name)
    try: documents = PyMuPDFLoader(str(path)).load()
    finally: path.unlink(missing_ok=True)
    for doc in documents: doc.metadata.update({"source_type":"pdf", "file_name":upload.filename or "upload.pdf", "timestamp":datetime.now(timezone.utc).isoformat()})
    return split_documents(documents)
def read_url(url):
    documents = WebBaseLoader(url).load()
    for doc in documents: doc.metadata.update({"source_type":"url", "source":url, "timestamp":datetime.now(timezone.utc).isoformat()})
    return split_documents(documents)
