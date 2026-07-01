from app import crud, utils
from app.logger import logger
from app.config import settings
from sqlalchemy.orm import Session

def create_short_url(
    db: Session,
    original_url : str,
    custom_alias : str | None = None,
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

    url = crud.create_url(
        db=db,
        original_url=str(original_url),
        short_code=short_code,
    )

    logger.info(
        "Short URL created: %s -> %s",
        short_code,
        original_url,
    )

    return url