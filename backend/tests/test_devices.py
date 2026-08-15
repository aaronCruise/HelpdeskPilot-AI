def create_test_device(client):
    payload = {
        "asset_tag": "TEST-001",
        "name": "Test Device",
        "type": "computer",
    }

    response = client.post("/devices/", json=payload)
    assert response.status_code == 200
    return response.json()


def test_create_device(client):
    payload = create_test_device(client)
    assert payload["message"] == "device received"

    device = payload["device"]
    assert device["asset_tag"] == "TEST-001"
    assert device["name"] == "Test Device"
    assert device["type"] == "computer"
    assert device["state"] == "available"
    assert "created_at" in device


def test_create_device_validation(client):
    response = client.post(
        "/devices/",
        json={"asset_tag": "", "name": "Test Device", "type": "computer"},
    )
    assert response.status_code == 422


def test_read_devices(client):
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


def test_read_device_by_id(client):
    device = create_test_device(client)["device"]

    response = client.get(f"/devices/{device['did']}")
    assert response.status_code == 200

    payload = response.json()
    assert payload["asset_tag"] == "TEST-001"
    assert payload["name"] == "Test Device"
    assert payload["type"] == "computer"
    assert payload["state"] == "available"


def test_read_nonexistent_device(client):
    device = create_test_device(client)["device"]

    response = client.get(f"/devices/{device['did'] + 1000000}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Device not found"}


def test_patch_device(client):
    device = create_test_device(client)["device"]

    response = client.patch(f"/devices/{device['did']}", json={"state": "maintenance"})
    assert response.status_code == 200

    payload = response.json()
    assert payload["state"] == "maintenance"


def test_nonexistent_device_patch(client):
    device = create_test_device(client)["device"]

    response = client.patch(f"/devices/{device['did'] + 1000000}", json={"state": "maintenance"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Device not found"}