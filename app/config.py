import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SHORT_CODE_LENGTH: int = int(os.getenv("SHORT_CODE_LENGTH", 6))

    UPSTASH_REDIS_REST_URL : str = os.getenv("UPSTASH_REDIS_REST_URL", "localhost")
    UPSTASH_REDIS_REST_TOKEN : str = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    print(UPSTASH_REDIS_REST_TOKEN, UPSTASH_REDIS_REST_URL)
    REDIS_PORT : int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB : int = int(os.getenv("REDIS_DB", 0))
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL")


settings = Settings()