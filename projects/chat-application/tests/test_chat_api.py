"""Integration tests for authenticated rooms and persisted message history."""
import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))
pytest.importorskip("flask")
from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "DATABASE": str(tmp_path / "chat.sqlite3"),
        "SECRET_KEY": "test-secret",
    })
    return app.test_client()


def register(client, username):
    response = client.post("/auth/register", json={"username": username, "password": "correct-horse"})
    assert response.status_code == 201
    return response.get_json()["id"]


def login(client, username):
    response = client.post("/auth/login", json={"username": username, "password": "correct-horse"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.get_json()['access_token']}"}


def test_room_membership_message_persistence_and_history(client):
    register(client, "alice")
    member_id = register(client, "bob")
    owner_headers = login(client, "alice")
    member_headers = login(client, "bob")

    room = client.post("/rooms", json={"name": "general"}, headers=owner_headers)
    assert room.status_code == 201
    room_id = room.get_json()["id"]

    denied = client.post(f"/rooms/{room_id}/messages", json={"body": "nope"}, headers=member_headers)
    assert denied.status_code == 403
    assert client.post(
        f"/rooms/{room_id}/members", json={"user_id": member_id}, headers=owner_headers
    ).status_code == 200

    first = client.post(f"/rooms/{room_id}/messages", json={"body": "hello"}, headers=member_headers)
    second = client.post(f"/rooms/{room_id}/messages", json={"body": "world"}, headers=owner_headers)
    assert first.status_code == second.status_code == 201
    assert first.get_json()["sender_username"] == "bob"

    # A fresh app instance proves messages are stored in SQLite, not process memory.
    reopened = create_app({
        "TESTING": True,
        "DATABASE": client.application.config["DATABASE"],
        "SECRET_KEY": "test-secret",
    }).test_client()
    history = reopened.get(f"/rooms/{room_id}/messages", headers=member_headers)
    assert history.status_code == 200
    assert [item["body"] for item in history.get_json()["messages"]] == ["hello", "world"]


def test_authentication_and_room_owner_authorization(client):
    register(client, "owner")
    register(client, "outsider")
    owner_headers = login(client, "owner")
    outsider_headers = login(client, "outsider")
    room_id = client.post("/rooms", json={"name": "private"}, headers=owner_headers).get_json()["id"]

    assert client.get(f"/rooms/{room_id}/messages").status_code == 401
    assert client.post(
        f"/rooms/{room_id}/members",
        json={"user_id": 1},
        headers=outsider_headers,
    ).status_code == 403
    assert client.get(f"/rooms/{room_id}/messages", headers=outsider_headers).status_code == 403


def test_message_validation_and_cursor_pagination(client):
    register(client, "alice")
    headers = login(client, "alice")
    room_id = client.post("/rooms", json={"name": "general"}, headers=headers).get_json()["id"]

    assert client.post(f"/rooms/{room_id}/messages", json={"body": "  "}, headers=headers).status_code == 400
    for body in ("one", "two", "three"):
        assert client.post(f"/rooms/{room_id}/messages", json={"body": body}, headers=headers).status_code == 201

    page = client.get(f"/rooms/{room_id}/messages?limit=2", headers=headers).get_json()
    assert [message["body"] for message in page["messages"]] == ["two", "three"]
    older = client.get(
        f"/rooms/{room_id}/messages?limit=2&before_id={page['next_before_id']}",
        headers=headers,
    ).get_json()
    assert [message["body"] for message in older["messages"]] == ["one"]


def test_duplicate_registration_and_invalid_pagination(client):
    register(client, "alice")
    assert client.post(
        "/auth/register", json={"username": "alice", "password": "correct-horse"}
    ).status_code == 409
    headers = login(client, "alice")
    room_id = client.post("/rooms", json={"name": "general"}, headers=headers).get_json()["id"]
    assert client.get(f"/rooms/{room_id}/messages?limit=0", headers=headers).status_code == 400
