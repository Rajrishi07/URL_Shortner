import time 
from fastapi import Request 
from starlette.middleware.base import BaseHTTPMiddleware 

from app.logger import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000 
        
            logger.info(
                "%s %s | %d | %.2f ms",
                request.method,
                request.url.path,
                locals().get("status_code", 500),
                duration_ms,
            )