
from fastapi import FastAPI, Response, status
from app.api import shorten, redirect, urls
from app.api.health import router as health_router

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
app.include_router(shorten.shorten_router, prefix="/api", tags=["Shorten_URLs"])
app.include_router(redirect.redirect_router, tags=["Redirect"])
app.include_router(urls.url_router, prefix="/urls", tags=["URLs"])
app.include_router(health_router)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/")
def root():
    return {"message": "URL Shortener API"}


