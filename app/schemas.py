from pydantic import BaseModel, HttpUrl, Field, field_validator, ConfigDict, model_validator
from datetime import datetime
import re
from enum import Enum


ALIAS_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")

class URLCreate(BaseModel):
    url: HttpUrl
    custom_alias : str | None = Field(
        default=None,
        min_length=3,
        max_length=20,
    )
    expires_in_days: int | None = None

    @field_validator("custom_alias")
    @classmethod
    def validate_custom_alias(cls, value: str | None) -> str | None:
        if value is None:
            return value

        pattern = r"^[a-zA-Z0-9_-]+$"

        if not ALIAS_PATTERN.fullmatch(value):
            raise ValueError(
                "Custom alias may only contain letters, numbers, '-' and '_'."
            )

        return value
    
    @field_validator("expires_in_days")
    @classmethod
    def validate_expires_in_days(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Expiration must be a positive integer.")
        return value


class URLResponse(BaseModel):
    id: int
    short_url: str
    expires_at: str | None = None


class URLAnalytics(BaseModel):
    original_url: str
    short_url: str
    clicks: int
    created_at: datetime
    last_accessed: datetime | None

class URLItem(BaseModel):
    id: int
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime
    expires_at: datetime | None
    last_accessed: datetime | None

    model_config = ConfigDict(from_attributes=True)

class URLListResponse(BaseModel):
    items: list[URLItem]
    page: int
    pages: int
    total: int

class URLSort(str, Enum):
    CREATED_AT_DESC = "created_at_desc"
    CREATED_AT_ASC = "created_at_asc"
    CLICKS_DESC = "clicks_desc"
    CLICKS_ASC = "clicks_asc"

class URLUpdateRequest(BaseModel):
    custom_alias: str | None = None
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def validate_not_empty(self):

        if (
            self.custom_alias is None
            and self.expires_at is None
        ):
            raise ValueError(
                "At least one field must be provided."
            )

        return self