from fastapi import Depends, APIRouter
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.database import get_db
from app.services import url_services

from app.logger import logger

redirect_router = APIRouter()

@redirect_router.get("/{short_code}")
def redirect_url(
    short_code : str,
    db: Session = Depends(get_db),
):
    logger.info("Redirect request for %s", short_code)
    
    url = url_services.resolve_short_url(db, short_code)
    logger.info(
        "Redirecting %s -> %s",
        short_code,
        url.original_url,
    )
    
    return RedirectResponse(
        url = url.original_url,
        status_code = 302
    )