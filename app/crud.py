from sqlalchemy.orm import Session
from app.models import URL
from sqlalchemy.sql import func

def create_url(
    db : Session,
    original_url: str,
    short_code: str
):
    url = URL(
        original_url=original_url,
        short_code=short_code
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
