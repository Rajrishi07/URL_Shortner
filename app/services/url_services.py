from app import crud, utils
from app.logger import logger
from app.config import settings

from app.domain import ResolvedURL
from sqlalchemy.orm import Session

from fastapi import HTTPException
from datetime import timezone, timedelta, datetime

import json

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
            raise ValueError(
                "Custom alias already exists."
            )

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

    if cached_url is not None:
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
        db_url = crud.get_url_by_short_code(db, short_code)
    
        if db_url is None:
            logger.warning("Short code %s not found", short_code)
            raise HTTPException(
                status_code = 404,
                detail = "Short URL not found"
            )
        
        url = model_to_domain(db_url)
        
        redis_client.setex(
            cache_key,
            CACHE_TTL,
            resolved_url_to_json(url),
        )
        #crud.increment_clicks(db, url.id)
    if (
            url.expires_at is not None
            and datetime.now(timezone.utc) >= url.expires_at
        ):
            logger.warning("Short code %s has expired", short_code)
            raise HTTPException(
                status_code = 410,
                detail = "Short URL has expired"
            )
    
    return ResolvedURL(
        id=url.id,
        short_code=url.short_code,
        original_url=url.original_url,
        expires_at=url.expires_at,
    )


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



def serialize_url(url):
    pass

def deserialize_url(data):
    pass

def model_to_domain(url):
    return ResolvedURL(
        id=url.id,
        short_code=url.short_code,
        original_url=url.original_url,
        expires_at=url.expires_at if url.expires_at else None
    )

def cache_to_domain():
    pass