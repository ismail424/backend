from pathlib import Path

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

root_router = APIRouter()
app = FastAPI(title="NextSalah API")


class CORSPreflightMiddleware(BaseHTTPMiddleware):
    """Handle CORS preflight requests before any redirects can occur."""
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return Response(
                status_code=204,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
                    "Access-Control-Max-Age": "86400",
                },
            )
        return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Must be added last to run first - handles OPTIONS before any redirects
app.add_middleware(CORSPreflightMiddleware)

@root_router.get("/", status_code=200)
def root(request: Request):

    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request},
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


