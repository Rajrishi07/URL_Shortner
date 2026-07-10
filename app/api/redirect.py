from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from datetime import timezone, datetime

from app.database import get_db
from app import crud

from app.logger import logger

redirect_router = APIRouter()

@redirect_router.get("/{short_code}")
def redirect_url(
    short_code : str,
    db: Session = Depends(get_db),
):
    logger.info("Redirect request for %s", short_code)
    url = crud.get_url_by_short_code(db, short_code)

    if url is None:
        logger.warning("Short code %s not found", short_code)
        raise HTTPException(
            status_code = 404,
            detail = "Short URL not found"
        )
    
    if (
        url.expires_at is not None
        and datetime.now(timezone.utc) >= url.expires_at
    ):
        logger.warning("Short code %s has expired", short_code)
        raise HTTPException(
            status_code = 410,
            detail = "Short URL has expired"
        )
    
    crud.increment_clicks(db, url.id)
    
    logger.info(
        "Redirecting %s -> %s",
        short_code,
        url.original_url,
    )
    
    return RedirectResponse(
        url = url.original_url,
        status_code = 302
    )