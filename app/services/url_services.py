from app import crud, utils
from app.logger import logger
from app.config import settings
from sqlalchemy.orm import Session

def create_short_url(
    db: Session,
    original_url : str
):
    exists =  crud.url_exists(db, str(original_url))
    if exists:
        logger.info("URL already exists for %s : Returning", original_url)
        return {
        "short_url": f"{settings.BASE_URL}/{exists.short_code}"
        }

    short_code = utils.generate_unique_short_code(db)

    crud.create_url(
        db=db,
        original_url=str(original_url),
        short_code=short_code,
    )

    logger.info(
        "Short URL created: %s -> %s",
        short_code,
        original_url,
    )

    return {
    "short_url": f"{settings.BASE_URL}/{short_code}"
    }