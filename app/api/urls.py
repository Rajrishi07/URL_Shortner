from fastapi import Response, Depends, APIRouter, Depends, Query, status, Request
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
    request: Request,
    db : Session = Depends(get_db),
):
    
    url = url_services.get_analytics(db, short_code)
    base_url = str(request.base_url).rstrip("/")
    return {
        "original_url": url.original_url,
        "short_url": f"{base_url}/{url.short_code}",
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
@url_router.patch(
    "/urls/{url_id}",
    response_model=schemas.URLItem,
)
def update_url(
    url_id: int,
    payload: schemas.URLUpdateRequest,
    db: Session = Depends(get_db),
):

    return url_services.update_url(
        db=db,
        url_id=url_id,
        payload=payload,
    )


@url_router.delete(
    "/urls/{url_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
):

    url_services.delete_url(
        db=db,
        url_id=url_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )

@url_router.get(
    "/dashboard",
    response_model=schemas.DashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
):
    return url_services.get_dashboard(db)