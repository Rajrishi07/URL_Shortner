import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.config import settings
from app.database import Base, get_db
from app.main import app

TEST_ENGINE = create_engine(settings.TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=TEST_ENGINE,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)



@pytest.fixture
def db():
    session = TestingSessionLocal()

    # clean database
    ...

    yield session

    session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def create_test_url(client, **kwargs):
    payload = {
        "url": "https://example.com",
        **kwargs,
    }

    return client.post(
        "/api/shorten",
        json=payload,
    )