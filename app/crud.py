from sqlalchemy.orm import Session
from app.models import URL
from sqlalchemy.sql import func

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