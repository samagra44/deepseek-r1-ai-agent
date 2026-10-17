import logging
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from app.core.config import get_settings
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    DocumentListResponse,
    DeleteResponse,
    HealthResponse,
    IngestResponse,
    UrlIngestRequest,
)
from app.services.agent import answer_question, search_web
from app.services.ingestion import read_pdf, read_url
from app.services.vector_store import (
    add_documents,
    retrieve,
    list_session_documents,
    delete_document,
    delete_session_documents,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["agent"])


def unavailable(error):
    return HTTPException(status_code=503, detail=str(error))


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", environment=get_settings().environment)


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        session = payload.session_id
        documents = (
            retrieve(payload.message, session_id=session) if payload.rag_enabled else []
        )
        context = "\n\n".join(documents)
        used_web = False
        if not context and payload.web_search_enabled:
            context = search_web(payload.message)
            used_web = bool(context)
        return ChatResponse(
            answer=answer_question(payload.message, context),
            sources_used=len(documents),
            used_web_search=used_web,
        )
    except ValueError as error:
        raise unavailable(error) from error
    except Exception as error:
        logger.exception("Chat endpoint failed")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate a response: {error}",
        ) from error


@router.post(
    "/documents/pdf", response_model=IngestResponse, status_code=status.HTTP_201_CREATED
)
async def ingest_pdf(
    file: UploadFile = File(...),
    session_id: str = Form("default"),
):
    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(status_code=415, detail="Only PDF files are supported.")
    try:
        docs = await read_pdf(file, get_settings().max_upload_size_mb * 1024 * 1024)
        return IngestResponse(
            source=file.filename or "upload.pdf",
            chunks_added=add_documents(docs, session_id=session_id),
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise unavailable(error) from error


@router.post(
    "/documents/url", response_model=IngestResponse, status_code=status.HTTP_201_CREATED
)
def ingest_url(payload: UrlIngestRequest):
    try:
        return IngestResponse(
            source=str(payload.url),
            chunks_added=add_documents(
                read_url(str(payload.url)),
                session_id=payload.session_id,
            ),
        )
    except Exception as error:
        raise unavailable(error) from error


@router.get("/documents", response_model=DocumentListResponse)
def list_docs(session_id: str = "default"):
    return DocumentListResponse(documents=list_session_documents(session_id))


@router.delete("/documents/{doc_id}", response_model=DeleteResponse)
def remove_document(doc_id: str):
    return DeleteResponse(deleted=delete_document(doc_id))


@router.delete("/documents", response_model=DeleteResponse)
def clear_session(session_id: str = "default"):
    return DeleteResponse(deleted=delete_session_documents(session_id))
