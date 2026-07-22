from fastapi import Depends, APIRouter, Depends, Query
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

@url_router.get(
    "/urls",
    response_model=schemas.URLListResponse,
)
def get_urls(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    sort: str = "created_at_desc",
    active_only: bool = False,
    db: Session = Depends(get_db),
):

    return url_services.list_urls(
        db=db,
        page=page,
        limit=limit,
        search=search,
        sort=sort,
        active_only=active_only,
    )

@url_router.get(
    "/urls/{url_id}",
    response_model=schemas.URLItem,
)
def get_url(
    url_id: int,
    db: Session = Depends(get_db),
):
    return url_services.get_url(
        db=db,
        url_id=url_id,
    )