from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class ResolvedURL:
    id : int
    short_code : str
    original_url : str
    expires_at : datetime | None