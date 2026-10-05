import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from app.core.config import get_settings

def chat_model() -> AzureChatOpenAI:
    settings = get_settings()
    if not settings.azure_openai_api_key or not settings.azure_openai_endpoint:
        raise ValueError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT must be configured.")
    return AzureChatOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version=settings.openai_api_version,
        azure_deployment=settings.azure_openai_deployment or settings.azure_model,
        temperature=0,
    )

def answer_question(question: str, context: str) -> str:
    response = chat_model().invoke([
        SystemMessage(content="Answer accurately using the supplied context. If it is insufficient, say so clearly. Use Markdown where helpful."),
        HumanMessage(content=f"Context:\n{context or 'No external context available.'}\n\nQuestion: {question}"),
    ])
    return re.sub(r"<think>.*?</think>", "", str(response.content), flags=re.DOTALL).strip()

def search_web(question: str) -> str:
    from duckduckgo_search import DDGS
    results = list(DDGS().text(question, max_results=5))
    if not results:
        return ""
    raw_results = "\n\n".join(f"Title: {item.get('title', '')}\nURL: {item.get('href', '')}\nSnippet: {item.get('body', '')}" for item in results)
    response = chat_model().invoke([
        SystemMessage(content="Summarize these web-search results factually. Preserve relevant source URLs."),
        HumanMessage(content=f"Question: {question}\n\nSearch results:\n{raw_results}"),
    ])
    return str(response.content).strip()
