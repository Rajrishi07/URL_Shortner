from app import crud, utils
from app.logger import logger
from app.config import settings
from app.schemas import URLItem, URLListResponse, URLSort

from app.domain import ResolvedURL
from app.exceptions.url import URLExpiredException, URLNotFoundException, URLIdNotFoundException, DuplicateAliasException
from sqlalchemy.orm import Session

from datetime import timezone, timedelta, datetime

import json
import math

from app.redis_client import redis_client

CACHE_PREFIX = "url:"
CACHE_TTL = 3600

def create_short_url(
    db: Session,
    original_url : str,
    custom_alias : str | None = None,
    expires_in_days : int | None = None,
):
    if custom_alias:
        existing = crud.get_url_by_short_code(
            db,
            custom_alias,
        )

        if existing:
            raise DuplicateAliasException(custom_alias)

        short_code = custom_alias
    else:
        exists =  crud.url_exists(db, str(original_url))
        if exists:
            logger.info("Short URL already exists for %s : Returning", original_url)
            return exists

        short_code = utils.generate_unique_short_code(db)
    
    expires_at = None
    if expires_in_days:
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)

    url = crud.create_url(
        db=db,
        original_url=str(original_url),
        short_code=short_code,
        expires_at=expires_at,
    )

    logger.info(
        "Short URL created: %s -> %s (Expires at: %s)",
        short_code,
        original_url,
        expires_at.isoformat() if expires_at else "Never",
    )

    return url

def resolve_short_url(db: Session, short_code: str):
    cache_key = f"{CACHE_PREFIX}{short_code}"
    cached_url = redis_client.get(cache_key)

    if cached_url:
        logger.info(
            "Cache HIT for %s",
            short_code,
        )
        url = json_to_resolved_url(cached_url)
    else:
        logger.info(
            "Cache MISS for %s",
            short_code,
        )
        model = crud.get_url_by_short_code(db, short_code)
    
        if model is None:
            logger.warning("Short code %s not found", short_code)
            raise URLNotFoundException(short_code)
        
        url = model_to_domain(model)
        
        redis_client.setex(
            cache_key,
            CACHE_TTL,
            resolved_url_to_json(url),
        )
    
    now = datetime.now(timezone.utc)
    if (
            url.expires_at is not None
            and now >= url.expires_at
        ):
            logger.warning("Short code %s has expired", short_code)
            raise URLExpiredException(short_code)
    crud.increment_clicks(db, url.id)
    return url


def resolved_url_to_json(url: ResolvedURL) -> str:
    data = {
        "id" : url.id,
        "short_code": url.short_code,
        "original_url" : url.original_url,
        "expires_at" : url.expires_at.isoformat() if url.expires_at else None
    }
    return json.dumps(data)

def json_to_resolved_url(data: str) -> ResolvedURL:
    url_dict = json.loads(data)
    expires_at = (
        datetime.fromisoformat(url_dict["expires_at"])
        if url_dict["expires_at"] is not None
        else None
    )

    return ResolvedURL(
        id=url_dict["id"],
        short_code=url_dict["short_code"],
        original_url=url_dict["original_url"],
        expires_at=expires_at,
    )


def model_to_domain(url):
    return ResolvedURL(
        id=url.id,
        short_code=url.short_code,
        original_url=url.original_url,
        expires_at=url.expires_at if url.expires_at else None
    )

def cache_to_domain():
    pass

def invalidate_url_cache(short_code: str) -> None:
    cache_key = f"{CACHE_PREFIX}{short_code}"
    redis_client.delete(cache_key)

    logger.info(
        "Cache invalidated for %s",
        short_code,
    )

def cleanup_expired_urls(db: Session) -> int:
    return crud.delete_expired_utls(db)

def get_analytics(db: Session, short_code):
    url = crud.get_url_by_short_code(db, short_code)

    if not url:
        raise URLNotFoundException(short_code)
    return url

def list_urls(
    db: Session,
    page: int,
    limit: int,
    search: str | None,
    sort: URLSort,
    active_only: bool,
) -> URLListResponse:

    urls, total = crud.get_urls(
        db=db,
        page=page,
        limit=limit,
        search=search,
        sort=sort,
        active_only=active_only,
    )

    pages = math.ceil(total / limit) if total else 0

    return URLListResponse(
        items=[
            URLItem.model_validate(url)
            for url in urls
        ],
        page=page,
        pages=pages,
        total=total,
    )

def get_url(
    db: Session,
    url_id: int,
) -> URLItem:

    url = crud.get_url_by_id(db, url_id)

    if url is None:
        raise URLIdNotFoundException(url_id)

    return URLItem.model_validate(url)