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
def create_test_device(client):
    payload = {
        "asset_tag": "TEST-001",
        "name": "Test Device",
        "type": "computer"
    }

    response = client.post("/devices/", json=payload)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_device():
    payload = create_test_device(client)
    assert payload["message"] == "device received"

    device = payload["device"]
    assert device["asset_tag"] == "TEST-001"
    assert device["name"] == "Test Device"
    assert device["type"] == "computer"
    assert device["state"] == "available"
    assert "created_at" in device

def test_create_device_validation():
    response = client.post(
        "/devices/",
        json={
            "asset_tag": "",
            "name": "Test Device",
            "type": "computer"
        }
    )
    assert response.status_code == 422

def test_read_devices():
    response = client.get("/devices/")
    assert response.status_code == 200

    payload = response.json()
    assert payload["message"] == "Querying all devices"
    assert isinstance(payload["devices"], list)

    if payload["devices"]:
        device = payload["devices"][0]
        assert "asset_tag" in device
        assert "name" in device
        assert "type" in device

def test_read_device_by_id():
    device = create_test_device(client)["device"]
    did = device["did"]

    response = client.get(f"/devices/{did}")
    assert response.status_code == 200

    payload = response.json()
    assert payload["asset_tag"] == "TEST-001"
    assert payload["name"] == "Test Device"
    assert payload["type"] == "computer"
    assert payload["state"] == "available"

def test_read_nonexistent_device():
    device = create_test_device(client)["device"]
    nonexistent_did = device["did"] + 1000000

    response = client.get(f"/devices/{nonexistent_did}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Device not found"}

def test_patch_device():
    device = create_test_device(client)["device"]
    did = device["did"]

    response = client.patch(f"/devices/{did}", json={"state": "maintenance"})
    assert response.status_code == 200

    payload = response.json()
    assert payload["state"] == "maintenance"

def test_nonexistent_device_patch():
    device = create_test_device(client)["device"]
    nonexistent_did = device["did"] + 1000000

    response = client.patch(f"/devices/{nonexistent_did}", json={"state": "maintenance"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Device not found"}