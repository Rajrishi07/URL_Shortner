from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.redis_client import redis_client

redis_client.ping()

from app.database import get_db
from app.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }

@router.get("/ready")
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

    try:
        redis_client.ping()

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Redis unavailable"
        )

    return {
        "status": "ready"
    }