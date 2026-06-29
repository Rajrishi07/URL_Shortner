
from fastapi import FastAPI
from app.database import Base, engine
from app.api import shorten, redirect

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(shorten.shorten_router, prefix="/api", tags=["URLs"])
app.include_router(redirect.redirect_router, tags=["Redirect"])

@app.get("/")
def root():
    return {"message": "URL Shortener API"}

