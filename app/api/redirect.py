from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

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
    
    logger.info(
        "Redirecting %s -> %s",
        short_code,
        url.original_url,
    )
    
    return RedirectResponse(
        url = url.original_url,
        status_code = 302
    )