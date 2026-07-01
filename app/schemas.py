from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    short_url: str


class URLAnalytics(BaseModel):
    original_url: str
    short_url: str
    clicks: int
    created_at: datetime
    last_accessed: datetime | None