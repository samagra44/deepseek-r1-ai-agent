import re
import os
from agno.agent import Agent
# from config.node import TOGETHER_AI_API_KEY
# from config.node import TOGETHER_AI_MODEL
# from config.node import OPENROUTER_MODEL
# from config.node import OPENROUTER_API_KEY
from agno.models.together import Together
from agno.models.openrouter import OpenRouter
import streamlit as st

TOGETHER_AI_API_KEY = st.secrets["TOGETHER_AI_API_KEY"]
TOGETHER_AI_MODEL = st.secrets["TOGETHER_AI_MODEL"]

os.environ['OPENAI_API_KEY'] = TOGETHER_AI_API_KEY

# os.environ['OPENAI_API_KEY'] = OPENROUTER_API_KEY

def filter_think_tags(response):
    """Remove content within <think> tags from the response."""
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)

def get_rag_agents():
    """Create a RAG Agent"""
    return Agent(
        name="DeepSeek RAG Agent",
        model=Together(id=TOGETHER_AI_MODEL),
        instructions="Answer using the most relevant information from the web search results. If you don't know the answer, say 'I don't know'.",
        markdown=True
    )

# def get_rag_agents():
#     """Create a RAG Agent"""
#     return Agent(
#         name="DeepSeek RAG Agent",
#         model=OpenRouter(id=OPENROUTER_MODEL),
#         instructions="Answer using the most relevant information from the web search results. If you don't know the answer, say 'I don't know'.",
#         markdown=True
#     )

# if __name__ == "__main__":
#     rag_agent = get_rag_agents()
#     rag_agent.print_response("What are the latest advancements in AI?")