from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200