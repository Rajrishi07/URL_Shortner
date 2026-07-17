from fastapi import Depends, APIRouter, Depends
from sqlalchemy.orm import Session


from app.exceptions.url import URLNotFoundException
from app.database import get_db
from app import schemas, crud
from app.config import settings
from app.services import url_services
url_router = APIRouter()

@url_router.get(
    "/analytics/{short_code}",
    response_model=schemas.URLAnalytics
)
def get_analytics(
    short_code : str,
    db : Session = Depends(get_db),
):
    
    url = url_services.get_analytics(db, short_code)
    
    return {
        "original_url": url.original_url,
        "short_url": f"{settings.BASE_URL}/{url.short_code}",
        "clicks": url.clicks,
        "created_at": url.created_at,
        "last_accessed": url.last_accessed,
    }