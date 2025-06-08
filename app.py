import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
import streamlit as st
from utils.rag_agents import *
from utils.web_agents import *
from helper.pdf_ingestion import *
from helper.url_ingestion import *
from backend.chroma_db import *
from helper.split_document_chunks import *

st.title("🐋 DeepSeek RAG Agent")
session_defaults = {
  "chroma_path": "./chroma_db",
  "model_version": "deepseek",
  "vector_store": None,
  "processed_documents": [],
  "history": [],
  "use_web_search": False,
  "force_web_search": False,
  "similarity_threshold": 0.7,
  "rag_enabled": True,
}

for key, value in session_defaults.items():
  if key not in st.session_state:
    st.session_state[key] = value

st.sidebar.header("🤖 Set Agent Configuration")
st.session_state.model_version = st.sidebar.radio("Select Model Version", ["Deepseek-R1"], help="DeepSeek Model is used.")

st.sidebar.header("🔍 Set RAG Configuration")
st.session_state.rag_enabled = st.sidebar.toggle("Enable RAG Mode", value=st.session_state.rag_enabled)

if st.sidebar.button("🗑️ Clear Chat"):
  st.session_state.history = []
  st.rerun()

st.sidebar.header("🌐 Set Web Search Configuration")
st.session_state.use_web_search = st.sidebar.checkbox("Enable Web Search Fallback", value=st.session_state.use_web_search)

st.sidebar.caption("Made by Samagra Shrivastava with ❤️")

def retrieve_documents(prompt, vector_store, COLLECTION_NAME, similarity_threshold):
    vector_store = chroma_client.client.get_collection(name=COLLECTION_NAME)
    results = vector_store.query(query_texts=[prompt], n_results=5)
    docs = results.get('documents', [])
    has_docs = len(docs) > 0
    return docs, has_docs

prompt = st.chat_input("Ask your query..." if st.session_state.rag_enabled else "Type your query here...")

if st.session_state.rag_enabled:
  chroma_client = init_chroma()

  st.sidebar.header("📁 Data Upload")
  uploaded_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
  web_url = st.sidebar.text_input("Or enter a URL")

  if uploaded_file and uploaded_file.name not in st.session_state.processed_documents:
    data = process_pdf(uploaded_file)
    if data:
      ids = [str(i) for i in range(len(data))]
      texts = [doc.page_content for doc in data]
      metadatas = [doc.metadata for doc in data]

      collection = chroma_client.client.get_collection(name=COLLECTION_NAME)
      collection.add(ids=ids, documents=texts, metadatas=metadatas)

      st.session_state.processed_documents.append(uploaded_file.name)

  if web_url and web_url not in st.session_state.processed_documents:
    texts = process_web(web_url)
    if texts:
      ids = [str(i) for i in range(len(texts))]
      texts_data = [doc.page_content for doc in texts]
      metadatas = [doc.metadata for doc in texts]

      collection = chroma_client.client.get_collection(name=COLLECTION_NAME)
      collection.add(ids=ids, documents=texts_data, metadatas=metadatas)

      st.session_state.processed_documents.append(web_url)

if prompt:
  st.session_state.history.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.write(prompt)

  context, docs = "", []
  if not st.session_state.force_web_search and st.session_state.rag_enabled:
    docs, has_docs = retrieve_documents(prompt, chroma_client, COLLECTION_NAME, st.session_state.similarity_threshold)
    if has_docs:
      flattened_docs = [paragraph for doc in docs for paragraph in doc]

      context = "\n\n".join(flattened_docs)

  if (st.session_state.force_web_search or not context) and st.session_state.use_web_search:
    with st.spinner("🔍 Searching the web..."):
      web_search_agent = get_web_search_agent()
      web_results = web_search_agent.run(prompt).content
      if web_results:
        context = f"Web Search Results:\n{web_results}"

  with st.spinner("🤖 Generating response..."):
    rag_agent = get_rag_agents()
    response = rag_agent.run(f"Context: {context}\n\nQuestion: {prompt}").content

    st.session_state.history.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
      st.write(filter_think_tags(response))

else:
  st.info("Agent is ready to answer!")