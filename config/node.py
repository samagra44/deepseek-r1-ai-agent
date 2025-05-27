import os

# Set the environment variable for the OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

# Set the environment variable for the Together AI API key
TOGETHER_AI_MODEL = os.getenv("TOGETHER_AI_MODEL")
TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")

COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Set the environment variable for the Google API key
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set the environment variable for the Hugging Face API key
HUGGINGFACE_EMBEDDING_MODEL = os.getenv("HUGGINGFACE_EMBEDDING_MODEL")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")