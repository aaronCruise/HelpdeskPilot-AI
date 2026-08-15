import pytest
from fastapi.testclient import TestClient
from backend.config import settings

# Override database URL for tests
settings.DATABASE_URL = settings.TEST_DATABASE_URL

from backend.database import Base, engine
from backend.main import app

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client