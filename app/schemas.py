from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class URLCreate(BaseModel):
    url: HttpUrl
    custom_alias : str | None = Field(
        default=None,
        min_length=3,
        max_length=20,
    )


class URLResponse(BaseModel):
    short_url: str


class URLAnalytics(BaseModel):
    original_url: str
    short_url: str
    clicks: int
    created_at: datetime
    last_accessed: datetime | None

