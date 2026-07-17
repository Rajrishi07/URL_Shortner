import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base

from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db

TEST_ENGINE = create_engine(
    settings.TEST_DATABASE_URL
)

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
    
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
        app.dependency_overrides.clear()
