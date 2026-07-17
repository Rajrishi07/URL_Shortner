from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.url_services import cleanup_expired_urls
from app.logger import logger

scheduler = BackgroundScheduler()


def cleanup_job() -> None:
    db: Session = SessionLocal()

    try:
        deleted = cleanup_expired_urls(db)

        if deleted:
          logger.info(
              "[Scheduler] Deleted %s expired URL(s).",
                deleted
                )

    finally:
        db.close()


def start_scheduler() -> None:
    if scheduler.running:
        return 
    scheduler.add_job(
        cleanup_job,
        trigger="interval",
        hours=2,
        id="cleanup_expired_urls",
        replace_existing=True,
    )

    scheduler.start()
    cleanup_job()


def stop_scheduler() -> None:
    """
    Gracefully stop the scheduler.
    """
    if scheduler.running:
        scheduler.shutdown(wait=False)