import os
import pytest
from fastapi.testclient import TestClient
from backend.paths import TEST_DB_FILE

os.environ["HDPILOT_DB_URL"] = f"sqlite:///{TEST_DB_FILE}"

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