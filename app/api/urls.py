from fastapi import Depends, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud
from app.config import settings
url_router = APIRouter()

@url_router.get(
    "/analytics/{short_code}",
    response_model=schemas.URLAnalytics
)
def get_analytics(
    short_code : str,
    db : Session = Depends(get_db),
):
    url = crud.get_url_by_short_code(db, short_code)

    if url is None:
        raise HTTPException(
            status_code=404,
            details="Short URL not found",
        )
    
    return {
        "original_url": url.original_url,
        "short_url": f"{settings.BASE_URL}/{url.short_code}",
        "clicks": url.clicks,
        "created_at": url.created_at,
        "last_accessed": url.last_accessed,
    }