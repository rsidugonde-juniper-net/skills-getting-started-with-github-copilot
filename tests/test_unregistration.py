from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_unregister_existing_participant():
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Ensure starting state has the participant
    assert email in activities[activity]["participants"]

    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
    assert "Unregistered" in resp.json().get("message", "")


def test_unregister_not_signed_up():
    activity = "Chess Club"
    email = "notpresent@example.com"

    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 400


def test_sign_up_and_unregister_roundtrip():
    activity = "Gym Class"
    email = "tempuser@example.com"

    # sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # unregister
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
