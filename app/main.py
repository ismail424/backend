from pathlib import Path

from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

root_router = APIRouter()
app = FastAPI(title="NextSalah API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@root_router.get("/", status_code=200)
def root(request: Request):

    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request},
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


