from sqlalchemy.orm import Session
from app.models import URL

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


def short_code_exists(
    db : Session, 
    short_code : str
) -> bool:
    return (
        db.query(URL)
        .filter(URL.short_code == short_code)
        .first()
        is not None
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