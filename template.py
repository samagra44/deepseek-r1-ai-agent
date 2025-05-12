import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_of_files = [
    ".github",
    "helper/__init__.py",
    "helper/pdf_ingestion.py",
    "helper/url_ingestion.py",
    "config/__init__.py",
    "config/node.py",
    "utils/__init__.py",
    "utils/web_agents.py",
    "utils/rag_agents.py",
    "backend/__init__.py",
    "tests/test.py",
    "backend/chroma_db.py",
    "app.py",
    "requirements.txt",
    "README.md",
    ".env",
    ".gitignore",
    "setup.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as file:
            pass
        logging.info(f"Created file: {filepath}")
    
    else:
        logging.info(f"File already exists: {filepath}")