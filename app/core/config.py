from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "DeepSeek RAG Agent"
    environment: str = "development"
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    openai_api_version: str = "2023-05-15"
    azure_openai_deployment: str | None = None
    azure_model: str = "gpt-4o"
    azure_openai_embedding_api_key: str | None = None
    azure_openai_embedding_deployment_name: str | None = None
    azure_openai_resource_name: str | None = None
    collection_name: str = "deepseek_rag"
    chroma_path: Path = Path("./data/chroma")
    max_upload_size_mb: int = Field(default=20, ge=1, le=100)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
