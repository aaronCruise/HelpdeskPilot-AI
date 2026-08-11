from types import SimpleNamespace

from app.models.ticket import CATEGORIES, PRIORITIES, STATUSES


def create_test_ticket(client, custom_text="This is a test ticket for the test_ticket suite."):
    payload = {
        "requester_name": "Test Name",
        "requester_email": "test@domain.com",
        "text": custom_text,
    }

    response = client.post("/tickets/", json=payload)
    assert response.status_code == 200
    return response.json()


def test_create_ticket(client):
    payload = create_test_ticket(client)
    assert payload["message"] == "Ticket received"

    ticket = payload["ticket"]
    assert ticket["requester_name"] == "Test Name"
    assert ticket["requester_email"] == "test@domain.com"
    assert ticket["text"] == "This is a test ticket for the test_ticket suite."
    assert ticket["category"] == CATEGORIES.GENERAL.value
    assert ticket["priority"] == PRIORITIES.MEDIUM.value
    assert ticket["status"] == STATUSES.NEW.value
    assert "created_at" in ticket


def test_create_ticket_validation(client):
    response = client.post(
        "/tickets/",
        json={
            "requester_name": "Test Name",
            "requester_email": "not-an-email",
            "text": "This is a test ticket for the test_ticket suite.",
        },
    )
    assert response.status_code == 422


def test_read_tickets(client):
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


def test_read_ticket_by_id(client):
    ticket = create_test_ticket(client)["ticket"]

    response = client.get(f"/tickets/{ticket['tid']}")
    assert response.status_code == 200

    payload = response.json()
    assert payload["requester_name"] == "Test Name"
    assert payload["requester_email"] == "test@domain.com"
    assert payload["text"] == "This is a test ticket for the test_ticket suite."


def test_read_nonexistent_ticket(client):
    ticket = create_test_ticket(client)["ticket"]

    response = client.get(f"/tickets/{ticket['tid'] + 1000000}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_patch_ticket(client):
    ticket = create_test_ticket(client)["ticket"]

    response = client.patch(
        f"/tickets/{ticket['tid']}",
        json={"status": STATUSES.IN_PROGRESS.value, "priority": PRIORITIES.HIGH.value},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == STATUSES.IN_PROGRESS.value
    assert payload["priority"] == PRIORITIES.HIGH.value


def test_nonexistent_ticket_patch(client):
    ticket = create_test_ticket(client)["ticket"]

    response = client.patch(
        f"/tickets/{ticket['tid'] + 1000000}",
        json={"status": STATUSES.IN_PROGRESS.value, "priority": PRIORITIES.HIGH.value},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_llm_analyze_ticket_no_api_key(monkeypatch):
    from app.services import llm_service

    class DummyMessage:
        content = '{"category":"network","priority":"high","summary":"Test summary","recommended_step":"Check Wi-Fi settings"}'

    class DummyResponse:
        message = DummyMessage()

    def fake_chat(**kwargs):
        return DummyResponse()

    monkeypatch.setattr(llm_service, "chat", fake_chat)

    ticket = SimpleNamespace(
        text="The Wi-Fi is down.",
        category=CATEGORIES.GENERAL,
        priority=PRIORITIES.MEDIUM,
    )

    recommendation = llm_service.llm_analyze_ticket_no_api_key(ticket, ["Wi-Fi policy"])

    assert recommendation.category == CATEGORIES.NETWORK
    assert recommendation.priority == PRIORITIES.HIGH
    assert recommendation.summary == "Test summary"
    assert recommendation.recommended_step == "Check Wi-Fi settings"


def test_analyze_ticket(client):
    ticket = create_test_ticket(client, custom_text="Please fix my wifi now.")["ticket"]
    response = client.post(f"/tickets/{ticket['tid']}/analyze")
    assert response.status_code == 200

    payload = response.json()
    assert payload["category"] == CATEGORIES.NETWORK.value
    assert payload["priority"] == PRIORITIES.HIGH.value
    assert "summary" in payload
    assert "recommended_step" in payload


def test_nonexistent_ticket_analyze(client):
    ticket = create_test_ticket(client)["ticket"]

    response = client.post(f"/tickets/{ticket['tid'] + 1000000}/analyze")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}