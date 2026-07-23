from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app import crud, schemas, utils
from app.services import url_services

from app.logger import logger

shorten_router = APIRouter()

@shorten_router.post("/shorten", response_model=schemas.URLResponse)
def shorten(
    request : Request,
    payload : schemas.URLCreate,
    db: Session = Depends(get_db)
):
    logger.info("Creating short URL for %s", payload.url)
    url = url_services.create_short_url(
        db=db,
        original_url=str(payload.url),
        custom_alias=payload.custom_alias,
        expires_in_days=payload.expires_in_days,
    )
    
    base_url = str(request.base_url).rstrip("/")
    return schemas.URLResponse(
        id=url.id,
        short_url=f"{base_url}/{url.short_code}",
        expires_at=url.expires_at.isoformat() if url.expires_at else None,
    )

