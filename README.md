# DeepSeek RAG Agent

## Project Overview
      
This is a Retrieval-Augmented Generation (RAG) application built with Streamlit that combines document processing, web search capabilities, and AI-powered question answering. The project uses the DeepSeek model for generating responses and implements a sophisticated RAG system. A powerful Retrieval-Augmented Generation (RAG) application that combines document processing, web search capabilities, and AI-powered question answering.

## Core Components
       
1. Main Application ```(app.py)```
    
- Built with Streamlit for the user interface
- Implements a chat interface for user interactions
- Model selection (DeepSeek-R1)
- RAG mode toggle
- Web search fallback option
- Document upload capabilities
- URL ingestion
- Chat history management

2. Backend Components
   
### ChromaDB Integration ```(backend/chroma_db.py)```
- Vector database for storing and retrieving document embeddings
- Handles document collection management
- Implements similarity search functionality

3. Helper Modules   
   
### PDF Processing ```(helper/pdf_ingestion.py)```
- Handles PDF document parsing and processing
- URL Processing ```(helper/url_ingestion.py)```
- Manages web content ingestion
- Document Chunking ```(helper/split_document_chunks.py)```
- Implements document splitting strategies

4. Utility Modules

### RAG Agents ```(utils/rag_agents.py)```
- Implements the RAG pipeline
- Manages context retrieval and response generation
- Web Agents ```(utils/web_agents.py)```
- Handles web search functionality
- Implements web content processing

5. Dependencies
- The project relies on several key libraries:
- ```streamlit```: Web application framework
- ```langchain``` and related packages: For LLM integration and RAG implementation
- ```chromadb```: Vector database for document storage
- ```google-generativeai```: Google's AI model integration
- ```duckduckgo-search```: Web search capabilities
- ```beautifulsoup4```: Web scraping
- ```pymupdf```: PDF processing

6. Features
    
- Document Processing
- PDF upload and processing
- Web URL ingestion
- Document chunking and embedding
- RAG Implementation
- Context retrieval from uploaded documents
- Similarity-based document search
- Context-aware response generation
- Web Search Integration
- Fallback web search capability
- Web content processing
- Search result integration
- User Interface
- Clean, intuitive chat interface
- Configuration sidebar
- Document upload interface
- Chat history management
- Configuration Options
- Model selection
- RAG mode toggle
- Web search fallback
- Similarity threshold adjustment

7. Technical Implementation
    
1. Document Processing Pipeline
- Documents are split into chunks
- Chunks are embedded and stored in ChromaDB
- Similarity search is performed for relevant context
      
2. RAG Pipeline
- User query is processed
- Relevant context is retrieved from documents
- Context is combined with query for response generation
- Web search fallback if needed
    
3. Response Generation
- Uses DeepSeek model for response generation
- Incorporates retrieved context
- Handles both document-based and web-based responses
     
This project represents a sophisticated implementation of RAG technology, combining document processing, web search, and AI-powered question answering in a user-friendly interface.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/samagra44/deepseek-r1-ai-agent.git
cd deepseek-r1-ai-agent
```

### Step 2: Create and Activate Virtual Environment
```bash
# For Windows
python -m venv env
.\env\Scripts\activate

# For macOS/Linux
python -m venv env
source env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Setup
Create a `.env` file in the root directory with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
```

### Step 5: Initialize the Database
The application will automatically initialize the ChromaDB database on first run.

## Running the Application

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8501
```

## Usage

1. **Upload Documents**
   - Use the sidebar to upload PDF documents
   - Or enter a URL to process web content

2. **Configure Settings**
   - Select model version
   - Toggle RAG mode
   - Enable/disable web search fallback

3. **Start Chatting**
   - Type your questions in the chat input
   - The agent will respond using the uploaded documents and/or web search

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure ChromaDB is properly initialized
   - Check if the `chroma_db` directory exists and has proper permissions

2. **API Key Issues**
   - Verify your API keys are correctly set in the `.env` file
   - Ensure the environment variables are properly loaded

3. **Dependency Conflicts**
   - If you encounter dependency conflicts, try:
   ```bash
   pip uninstall -r requirements.txt
   pip install -r requirements.txt
   ```

### Getting Help
If you encounter any issues:
1. Check the error messages in the console
2. Verify all dependencies are correctly installed
3. Ensure your Python version is compatible (3.8+)

## Development

### Project Structure
```
├── app.py                 # Main application file
├── backend/              # Backend components
│   ├── chroma_db.py      # Vector database integration
│   └── __init__.py
├── helper/               # Helper modules
│   ├── pdf_ingestion.py
│   ├── url_ingestion.py
│   └── split_document_chunks.py
├── utils/                # Utility modules
│   ├── rag_agents.py
│   └── web_agents.py
├── tests/                # Test directory
├── config/               # Configuration files
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

### Running Tests
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request