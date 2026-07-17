RATE_LIMIT = 100
WINDOW_SECONDS = 60

RATE_LIMIT_PREFIX = "rate_limit:"

from fastapi import Request, HTTPException
from app.redis_client import redis_client

def check_rate_limit(
        request: Request,
):
    client_ip = request.client.host
    cache_key = (
        f"{RATE_LIMIT_PREFIX}{client_ip}"
    )
    requests = redis_client.incr(cache_key)
    if requests == 1:
        redis_client.expire(
            cache_key,
            WINDOW_SECONDS,
        )
    elif requests > RATE_LIMIT:
        raise HTTPException(
            status_code=409,
            detail="Rate limit Exceeded."
        )