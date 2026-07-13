import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    SHORT_CODE_LENGTH: int = int(os.getenv("SHORT_CODE_LENGTH", 6))
    REDIS_HOST : str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT : int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB : int = int(os.getenv("REDIS_DB", 0))


settings = Settings()