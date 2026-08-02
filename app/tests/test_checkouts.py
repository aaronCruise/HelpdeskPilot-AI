from app.models.checkout import STATUSES


def create_test_checkout(client):
    device_payload = {
        "asset_tag": "TEST-001",
        "name": "Test Device",
        "type": "computer",
    }
    device_response = client.post("/devices/", json=device_payload)
    assert device_response.status_code == 200
    device = device_response.json()["device"]

    payload = {
        "device_id": device["did"],
        "borrower_name": "Test Borrower",
        "borrower_email": "borrower@domain.com",
        "from_date": "2025-01-01T10:00:00",
        "to_date": "2025-01-02T10:00:00",
    }

    response = client.post("/checkouts/", json=payload)
    assert response.status_code == 200
    return response.json()


def test_create_checkout(client):
    payload = create_test_checkout(client)
    assert payload["message"] == "Checkout received"

    checkout = payload["checkout"]
    assert checkout["borrower_name"] == "Test Borrower"
    assert checkout["borrower_email"] == "borrower@domain.com"
    assert checkout["status"] == STATUSES.ACTIVE.value


def test_create_checkout_validation(client):
    response = client.post(
        "/checkouts/",
        json={
            "device_id": 1,
            "borrower_name": "Test Borrower",
            "borrower_email": "not-an-email",
            "from_date": "2025-01-01T10:00:00",
            "to_date": "2025-01-02T10:00:00",
        },
    )
    assert response.status_code == 422


def test_create_checkout_unavailable_device(client):
    device_payload = {
        "asset_tag": "TEST-001",
        "name": "Test Device",
        "type": "computer",
    }
    device_response = client.post("/devices/", json=device_payload)
    assert device_response.status_code == 200
    device = device_response.json()["device"]

    payload = {
        "device_id": device["did"],
        "borrower_name": "Test Borrower",
        "borrower_email": "borrower@domain.com",
        "from_date": "2025-01-01T10:00:00",
        "to_date": "2025-01-02T10:00:00",
    }

    first_response = client.post("/checkouts/", json=payload)
    assert first_response.status_code == 200

    second_response = client.post("/checkouts/", json=payload)
    assert second_response.status_code == 401
    assert second_response.json() == {"detail": "Device is not available"}


def test_read_checkouts(client):
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


def test_read_active_checkouts(client):
    create_test_checkout(client)

    response = client.get("/checkouts/active")
    assert response.status_code == 200

    payload = response.json()
    assert payload["message"] == "Querying active checkouts"
    assert isinstance(payload["checkouts"], list)

    if payload["checkouts"]:
        checkout = payload["checkouts"][0]
        assert checkout["status"] == STATUSES.ACTIVE.value


def test_read_checkout_by_id(client):
    checkout = create_test_checkout(client)["checkout"]

    response = client.get(f"/checkouts/{checkout['cid']}")
    assert response.status_code == 200

    payload = response.json()
    assert payload["borrower_name"] == "Test Borrower"
    assert payload["borrower_email"] == "borrower@domain.com"
    assert payload["status"] == STATUSES.ACTIVE.value


def test_read_nonexistent_checkout(client):
    checkout = create_test_checkout(client)["checkout"]

    response = client.get(f"/checkouts/{checkout['cid'] + 1000000}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Checkout not found"}


def test_patch_checkout(client):
    checkout = create_test_checkout(client)["checkout"]

    response = client.patch(
        f"/checkout/{checkout['cid']}",
        json={"to_date": "2025-01-03T10:00:00", "status": STATUSES.OVERDUE.value},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["to_date"] == "2025-01-03T10:00:00"
    assert payload["status"] == STATUSES.OVERDUE.value


def test_nonexistent_checkout_patch(client):
    checkout = create_test_checkout(client)["checkout"]

    response = client.patch(
        f"/checkout/{checkout['cid'] + 1000000}",
        json={"to_date": "2025-01-03T10:00:00", "status": STATUSES.OVERDUE.value},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Checkout not found"}


def test_check_in_checkout(client):
    checkout = create_test_checkout(client)["checkout"]

    response = client.post("/checkin", json={"cid": checkout["cid"], "status": STATUSES.RETURNED.value})
    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == STATUSES.RETURNED.value


def test_check_in_nonexistent_checkout(client):
    response = client.post("/checkin", json={"cid": 999999, "status": STATUSES.RETURNED.value})
    assert response.status_code == 404
    assert response.json() == {"detail": "Checkout not found"}