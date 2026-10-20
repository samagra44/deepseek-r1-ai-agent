from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.api.routes import router
from app.core.config import get_settings
BASE_DIR=Path(__file__).resolve().parent
templates=Jinja2Templates(directory=str(BASE_DIR/"templates"))
@asynccontextmanager
async def lifespan(_):
    get_settings().chroma_path.mkdir(parents=True,exist_ok=True)
    yield
app=FastAPI(title="DeepSeek RAG Agent",version="1.0.0",lifespan=lifespan)
app.mount("/static",StaticFiles(directory=str(BASE_DIR/"static")),name="static")
app.include_router(router)
@app.get("/",response_class=HTMLResponse,include_in_schema=False)
async def index(request: Request): return templates.TemplateResponse(request,"index.html",{"app_name":get_settings().app_name})
