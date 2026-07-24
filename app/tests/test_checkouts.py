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
def create_test_checkout(client):
    device_payload = {
        "asset_tag": "TEST-001",
        "name": "Test Device",
        "type": "computer"
    }
    device_response = client.post("/devices/", json=device_payload)
    assert device_response.status_code == 200
    device = device_response.json()["device"]

    payload = {
        "device_id": device["did"],
        "borrower_name": "Test Borrower",
        "borrower_email": "borrower@domain.com",
        "from_date": "2025-01-01T10:00:00",
        "to_date": "2025-01-02T10:00:00"
    }

    response = client.post("/checkouts/", json=payload)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_checkout():
    payload = create_test_checkout(client)
    assert payload["message"] == "Checkout received"

    checkout = payload["checkout"]
    assert checkout["borrower_name"] == "Test Borrower"
    assert checkout["borrower_email"] == "borrower@domain.com"
    assert checkout["status"] == "active"

def test_create_checkout_validation():
    response = client.post(
        "/checkouts/",
        json={
            "device_id": 1,
            "borrower_name": "Test Borrower",
            "borrower_email": "not-an-email",
            "from_date": "2025-01-01T10:00:00",
            "to_date": "2025-01-02T10:00:00"
        }
    )
    assert response.status_code == 422

def test_create_checkout_unavailable_device():
    device_payload = {
        "asset_tag": "TEST-001",
        "name": "Test Device",
        "type": "computer"
    }
    device_response = client.post("/devices/", json=device_payload)
    assert device_response.status_code == 200
    device = device_response.json()["device"]

    payload = {
        "device_id": device["did"],
        "borrower_name": "Test Borrower",
        "borrower_email": "borrower@domain.com",
        "from_date": "2025-01-01T10:00:00",
        "to_date": "2025-01-02T10:00:00"
    }

    first_response = client.post("/checkouts/", json=payload)
    assert first_response.status_code == 200

    second_response = client.post("/checkouts/", json=payload)
    assert second_response.status_code == 401
    assert second_response.json() == {"detail": "Device is not available"}

def test_read_checkouts():
    response = client.get("/checkouts/")
    assert response.status_code == 200

    payload = response.json()
    assert payload["message"] == "Querying all checkouts"
    assert isinstance(payload["checkouts"], list)

    if payload["checkouts"]:
        checkout = payload["checkouts"][0]
        assert "borrower_name" in checkout
        assert "borrower_email" in checkout
        assert "status" in checkout

def test_read_active_checkouts():
    create_test_checkout(client)

    response = client.get("/checkouts/active")
    assert response.status_code == 200

    payload = response.json()
    assert payload["message"] == "Querying active checkouts"
    assert isinstance(payload["checkouts"], list)

    if payload["checkouts"]:
        checkout = payload["checkouts"][0]
        assert checkout["status"] == "active"

def test_read_checkout_by_id():
    checkout = create_test_checkout(client)["checkout"]
    cid = checkout["cid"]

    response = client.get(f"/checkouts/{cid}")
    assert response.status_code == 200

    payload = response.json()
    assert payload["borrower_name"] == "Test Borrower"
    assert payload["borrower_email"] == "borrower@domain.com"
    assert payload["status"] == "active"

def test_read_nonexistent_checkout():
    checkout = create_test_checkout(client)["checkout"]
    nonexistent_cid = checkout["cid"] + 1000000

    response = client.get(f"/checkouts/{nonexistent_cid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Checkout not found"}

def test_patch_checkout():
    checkout = create_test_checkout(client)["checkout"]
    cid = checkout["cid"]

    response = client.patch(
        f"/checkout/{cid}",
        json={
            "to_date": "2025-01-03T10:00:00",
            "status": "overdue"
        }
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["to_date"] == "2025-01-03T10:00:00"
    assert payload["status"] == "overdue"

def test_nonexistent_checkout_patch():
    checkout = create_test_checkout(client)["checkout"]
    nonexistent_cid = checkout["cid"] + 1000000

    response = client.patch(
        f"/checkout/{nonexistent_cid}",
        json={
            "to_date": "2025-01-03T10:00:00",
            "status": "overdue"
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Checkout not found"}

def test_check_in_checkout():
    checkout = create_test_checkout(client)["checkout"]
    cid = checkout["cid"]

    response = client.post("/checkin", json={"cid": cid, "status": "returned"})
    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "returned"

def test_check_in_nonexistent_checkout():
    response = client.post("/checkin", json={"cid": 999999, "status": "returned"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Checkout not found"}