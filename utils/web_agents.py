import os
from agno.agent import Agent
from config.node import OPENROUTER_MODEL
from config.node import TOGETHER_AI_MODEL
from config.node import TOGETHER_AI_API_KEY
from config.node import OPENROUTER_API_KEY
from agno.models.together import Together
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools

#os.environ['OPENAI_API_KEY'] = OPENROUTER_API_KEY

os.environ['OPENAI_API_KEY'] = TOGETHER_AI_API_KEY

## Using OpenRouter Services
# def get_web_search_agent():
#     """Creates a web search agent using DuckDuckGo"""
#     return Agent(
#         name="Web Search Agent",
#         model=OpenRouter(id=OPENROUTER_MODEL),
#         tools=[DuckDuckGoTools()],
#         instructions="Search the web using DuckDuckgo and summarize key points.",
#         markdown=True
#     )

## Using TogetherAI Services
def get_web_search_agent():
    """Creates a web search agent using DuckDuckGo"""
    return Agent(
        name="Web Search Agent",
        model=Together(id=TOGETHER_AI_MODEL),
        tools=[DuckDuckGoTools()],
        instructions="Search the web using DuckDuckgo and summarize key points.",
        markdown=True
    )

# if __name__ == "__main__":
#     agent = get_web_search_agent()
#     agent.print_response("Share a 2 minute summary of the latest news on AI.")