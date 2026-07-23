'''
NOTICE: This test suite will reset the database.
TODO: Use a separate test database to avoid data loss.
'''

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

# Helper function for each test case
def create_test_ticket(client):
    payload = {
        "requester_name": "Test Name",
        "requester_email": "test@domain.com",
        "text": "This is a test ticket for the test_ticket suite."
    }

    response = client.post("/tickets/", json=payload)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_ticket():
    payload = create_test_ticket(client)
    assert payload["message"] == "Ticket received"

    ticket = payload["ticket"]
    assert ticket["requester_name"] == "Test Name"
    assert ticket["requester_email"] == "test@domain.com"
    assert ticket["text"] == "This is a test ticket for the test_ticket suite."
    assert ticket["category"] == "general"
    assert ticket["priority"] == "medium"
    assert ticket["status"] == "new"
    assert "created_at" in ticket # We can't assume the exact timestamp

def test_create_ticket_validation():
    response = client.post(
        "/tickets/",
        json={
            "requester_name": "Test Name",
            "requester_email": "not-an-email",
            "text": "This is a test ticket for the test_ticket suite."
        }
    )
    assert response.status_code == 422

def test_read_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200

    payload = response.json()
    assert payload["message"] == "Querying all tickets"
    assert isinstance(payload["tickets"], list)

    if payload["tickets"]:
        ticket = payload["tickets"][0]
        assert "requester_name" in ticket
        assert "requester_email" in ticket
        assert "text" in ticket

def test_read_ticket_by_id():
    ticket = create_test_ticket(client)["ticket"]
    tid = ticket["tid"]

    response = client.get(f"/tickets/{tid}")
    assert response.status_code == 200

    payload = response.json()
    assert payload["requester_name"] == "Test Name"
    assert payload["requester_email"] == "test@domain.com"
    assert payload["text"] == "This is a test ticket for the test_ticket suite."

def test_read_nonexistent_ticket():
    ticket = create_test_ticket(client)["ticket"]
    nonexistent_tid = ticket["tid"] + 1000000

    response = client.get(f"/tickets/{nonexistent_tid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}

def test_patch_ticket():
    ticket = create_test_ticket(client)["ticket"]
    tid = ticket["tid"]

    response = client.patch(f"/tickets/{tid}", json={
        "status": "in_progress",
        "priority": "high"})
    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "in_progress"
    assert payload["priority"] == "high"

def test_nonexistent_ticket_patch():
    ticket = create_test_ticket(client)["ticket"]
    nonexistent_tid = ticket["tid"] + 1000000

    response = client.patch(f"/tickets/{nonexistent_tid}", json={
        "status": "in_progress",
        "priority": "high"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}