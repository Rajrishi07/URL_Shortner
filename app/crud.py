from sqlalchemy.orm import Session
from app.models import URL
from sqlalchemy.sql import func
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.schemas import URLSort

from datetime import datetime, timezone

def create_url(
    db : Session,
    original_url: str,
    short_code: str,
    expires_at: datetime | None = None
):
    url = URL(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url


def get_url_by_short_code(
    db: Session,
    short_code: str
):
    return (
        db.query(URL)
        .filter(URL.short_code == short_code)
        .first()
    )


def url_exists(
    db : Session,
    original_url : str
) :
    return (
        db.query(URL)
        .filter(URL.original_url == original_url)
        .first()
    )


def increment_clicks(
    db: Session,
     url_id: int,
) -> None:
    db.query(URL).filter(URL.id == url_id).update(
        {
            URL.clicks: URL.clicks + 1,
            URL.last_accessed: func.now(),
        }
    )
    db.commit()


def delete_expired_utls(db: Session) -> int:
    deleted = (
        db.query(URL)
        .filter(
            URL.expires_at.is_not(None),
            URL.expires_at < datetime.now(timezone.utc),
        )
        .delete(synchronize_session=False)
    )
    db.commit()
    return deleted


def get_urls(
    db: Session,
    page: int,
    limit: int,
    search: str | None,
    sort: URLSort,
    active_only: bool,
) -> tuple[list[URL], int]:

    query = db.query(URL)

    # Search
    if search:
        query = query.filter(
            or_(
                URL.short_code.ilike(f"%{search}%"),
                URL.original_url.ilike(f"%{search}%"),
            )
        )

    # Active filter
    if active_only:
        now = datetime.now(timezone.utc)

        query = query.filter(
            or_(
                URL.expires_at.is_(None),
                URL.expires_at > now,
            )
        )
        
    #Shorting
    SORT_MAPPING = {
        URLSort.CREATED_AT_DESC: URL.created_at.desc(),
        URLSort.CREATED_AT_ASC: URL.created_at.asc(),
        URLSort.CLICKS_DESC: URL.clicks.desc(),
        URLSort.CLICKS_ASC: URL.clicks.asc(),
    }

    query = query.order_by(
        SORT_MAPPING[sort]
    )

    total = query.count()

    items = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return items, total


def get_url_by_id(
    db: Session,
    url_id: int,
) -> URL | None:

    return (
        db.query(URL)
        .filter(URL.id == url_id)
        .first()
    )

def update_url(
    db: Session,
    url: URL,
    *,
    custom_alias: str | None,
    expires_at: datetime | None,
) -> URL:
    if custom_alias is not None:
        url.short_code = custom_alias

    if expires_at is not None:
        url.expires_at = expires_at

    db.commit()
    db.refresh(url)

    return url

def delete_url(
    db: Session,
    url: URL,
):
    db.delete(url)
    db.commit()