# DeepSeek RAG Agent

A production-oriented FastAPI RAG application with a vanilla HTML, CSS, and JavaScript frontend.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Add Azure OpenAI and Hugging Face credentials to .env
uvicorn app.main:app --reload
```

Open http://localhost:8000. API docs are available at http://localhost:8000/docs.

## Structure

- `app/api`: FastAPI endpoints
- `app/core`: typed environment configuration
- `app/models`: request and response contracts
- `app/services`: agent, ingestion, and vector-store logic
- `app/templates` and `app/static`: browser UI

Endpoints: `GET /api/health`, `POST /api/chat`, `POST /api/documents/pdf`, and `POST /api/documents/url`.


