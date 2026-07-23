
from fastapi import FastAPI, Response, status
from app.api import shorten, redirect, urls
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router

from app.middleware.logging import RequestLoggingMiddleware
from app.exceptions.handlers import register_exception_handler
from contextlib import asynccontextmanager
from app.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()

app = FastAPI(
    title="URL Shortener",
    lifespan=lifespan
)

origins = [
    "https://url-shortener-frontend-lemon-rho.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handler(app)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(health_router)

app.include_router(
    shorten.shorten_router,
    prefix="/api",
    tags=["Shorten URLs"],
)

app.include_router(
    urls.url_router,
    prefix="/api",
    tags=["URL Management"],
)

app.include_router(
    redirect.redirect_router,
    tags=["Redirect"],
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/")
def root():
    return {"message": "URL Shortener API"}


