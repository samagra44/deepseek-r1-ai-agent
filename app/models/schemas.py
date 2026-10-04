from pydantic import BaseModel, Field, HttpUrl


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12_000)
    session_id: str = Field(default="default", min_length=1, max_length=64)
    rag_enabled: bool = True
    web_search_enabled: bool = False


class ChatResponse(BaseModel):
    answer: str
    sources_used: int = 0
    used_web_search: bool = False


class UrlIngestRequest(BaseModel):
    url: HttpUrl
    session_id: str = Field(default="default", min_length=1, max_length=64)


class IngestResponse(BaseModel):
    source: str
    chunks_added: int


class DocumentInfo(BaseModel):
    id: str
    source_type: str
    source_name: str
    timestamp: str
    chunk_count: int


class DocumentListResponse(BaseModel):
    documents: list[DocumentInfo]


class DeleteResponse(BaseModel):
    deleted: int


class HealthResponse(BaseModel):
    status: str
    environment: str
