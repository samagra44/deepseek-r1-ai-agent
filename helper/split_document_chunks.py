from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def split_texts(documents):
  """Splits documents into text chunks."""
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  split_docs = text_splitter.split_documents(documents)
  return [Document(page_content=chunk.page_content, metadata=chunk.metadata) for chunk in split_docs if chunk.page_content.strip()]