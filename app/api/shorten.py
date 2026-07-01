from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app import crud, schemas, utils
from app.services import url_services

from app.logger import logger

shorten_router = APIRouter()

@shorten_router.post("/shorten", response_model=schemas.URLResponse)
def shorten(
    request : schemas.URLCreate,
    db: Session = Depends(get_db)
):
    logger.info("Creating short URL for %s", request.url)
    try:
        url = url_services.create_short_url(
            db=db,
            original_url=str(request.url),
            custom_alias=request.custom_alias,
        )

        return schemas.URLResponse(
            short_url=f"{settings.BASE_URL}/{url.short_code}",
        )

    except ValueError as e:
        logger.warning("Error while creating short URL for %s", str(e))
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )