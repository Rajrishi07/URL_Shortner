
from fastapi import FastAPI
from app.api import shorten, redirect, urls


app = FastAPI()
app.include_router(shorten.shorten_router, prefix="/api", tags=["Shorten_URLs"])
app.include_router(redirect.redirect_router, tags=["Redirect"])
app.include_router(urls.url_router, prefix="/urls", tags=["URLs"])

@app.get("/")
def root():
    return {"message": "URL Shortener API"}

