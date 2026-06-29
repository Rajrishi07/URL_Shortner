from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.config import settings
from app import crud, schemas, utils

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "URL Shortener API"}

@app.post("/shorten", response_model=schemas.URLResponse)
def shorten(
    request : schemas.URLCreate,
    db: Session = Depends(get_db)
):
    short_code = utils.generate_unique_short_code(db)

    crud.create_url(
        db=db,
        original_url=str(request.url),
        short_code=short_code,
    )

    return {
    "short_url": f"{settings.BASE_URL}/{short_code}"
    }
    