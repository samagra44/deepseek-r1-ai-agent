from functools import lru_cache
from uuid import uuid4
from agno.vectordb.chroma import ChromaDb
from langchain_openai import AzureOpenAIEmbeddings
from app.core.config import get_settings
from app.models.schemas import DocumentInfo


@lru_cache
def get_embeddings() -> AzureOpenAIEmbeddings:
    settings = get_settings()
    if not all(
        (
            settings.azure_openai_embedding_api_key,
            settings.azure_openai_embedding_deployment_name,
            settings.azure_openai_resource_name,
        )
    ):
        raise ValueError(
            "AZURE_OPENAI_EMBEDDING_API_KEY, AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME, "
            "and AZURE_OPENAI_RESOURCE_NAME must be configured."
        )
    return AzureOpenAIEmbeddings(
        azure_endpoint=f"https://{settings.azure_openai_resource_name}.openai.azure.com/",
        api_key=settings.azure_openai_embedding_api_key,
        azure_deployment=settings.azure_openai_embedding_deployment_name,
        api_version=settings.openai_api_version,
    )


@lru_cache
def get_vector_store():
    settings = get_settings()
    store = ChromaDb(
        collection=settings.collection_name,
        path=str(settings.chroma_path),
        persistent_client=True,
    )
    try:
        store.client.get_collection(name=settings.collection_name)
    except Exception:
        store.create()
    return store


def _collection():
    return get_vector_store().client.get_collection(name=get_settings().collection_name)


def add_documents(documents, session_id="default"):
    if not documents:
        return 0
    collection = _collection()
    for doc in documents:
        doc.metadata["session_id"] = session_id
    contents = [d.page_content for d in documents]
    collection.add(
        ids=[str(uuid4()) for _ in documents],
        documents=contents,
        embeddings=get_embeddings().embed_documents(contents),
        metadatas=[d.metadata for d in documents],
    )
    return len(documents)


def retrieve(query, session_id="default", limit=5):
    try:
        result = _collection().query(
            query_embeddings=[get_embeddings().embed_query(query)],
            n_results=limit,
            where={"session_id": session_id},
        )
        docs = result.get("documents", [[]])[0]
        return docs if docs else []
    except Exception:
        return []


def list_session_documents(session_id="default"):
    collection = _collection()
    all_data = collection.get(where={"session_id": session_id})
    if not all_data or not all_data.get("ids"):
        return []
    seen = {}
    for idx, doc_id in enumerate(all_data["ids"]):
        meta = (all_data.get("metadatas") or [{}])[idx] or {}
        source_type = meta.get("source_type", "unknown")
        source_name = meta.get("file_name") or meta.get("source", "unknown")
        ts = meta.get("timestamp", "")
        key = (source_type, source_name)
        if key not in seen:
            seen[key] = {
                "id": doc_id,
                "source_type": source_type,
                "source_name": source_name,
                "timestamp": ts,
                "chunk_count": 0,
            }
        seen[key]["chunk_count"] += 1
    return [DocumentInfo(**v) for v in seen.values()]


def delete_document(doc_id):
    _collection().delete(ids=[doc_id])
    return 1


def delete_session_documents(session_id="default"):
    collection = _collection()
    all_data = collection.get(where={"session_id": session_id})
    ids = all_data.get("ids", [])
    if ids:
        collection.delete(ids=ids)
    return len(ids)
