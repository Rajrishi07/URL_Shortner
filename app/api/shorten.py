from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app import crud, schemas, utils

from app.logger import logger

shorten_router = APIRouter()

@shorten_router.post("/shorten", response_model=schemas.URLResponse)
def shorten(
    request : schemas.URLCreate,
    db: Session = Depends(get_db)
):
    logger.info("Creating short URL for %s", request.url)
    exists =  crud.url_exists(db, str(request.url))
    if exists:
        logger.info("URL already exists for %s : Returning", request.url)
        return {
        "short_url": f"{settings.BASE_URL}/{exists.short_code}"
        }

    short_code = utils.generate_unique_short_code(db)

    crud.create_url(
        db=db,
        original_url=str(request.url),
        short_code=short_code,
    )

    logger.info(
        "Short URL created: %s -> %s",
        short_code,
        request.url,
    )

    return {
    "short_url": f"{settings.BASE_URL}/{short_code}"
    }