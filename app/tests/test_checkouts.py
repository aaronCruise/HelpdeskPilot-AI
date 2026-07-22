from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_checkouts():
    response = client.get("/checkouts/")
    assert response.status_code == 200