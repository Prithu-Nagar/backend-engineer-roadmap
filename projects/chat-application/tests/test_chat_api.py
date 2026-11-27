"""Integration tests for authenticated rooms and persisted message history."""
import json
import sys
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest
from simple_websocket import Client as WebSocketClient
from simple_websocket.errors import ConnectionClosed
from werkzeug.serving import make_server

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


@pytest.fixture
def websocket_url(client):
    server = make_server("127.0.0.1", 0, client.application, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"ws://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


@contextmanager
def connect_websocket(url):
    websocket = WebSocketClient.connect(url)
    try:
        yield websocket
    finally:
        try:
            websocket.close()
        except ConnectionClosed:
            pass


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



def test_rest_message_client_id_is_idempotent(client):
    register(client, "alice")
    headers = login(client, "alice")
    room_id = client.post("/rooms", json={"name": "general"}, headers=headers).get_json()["id"]
    payload = {"body": "retry-safe", "client_message_id": "client-1"}
    first = client.post(f"/rooms/{room_id}/messages", json=payload, headers=headers)
    retry = client.post(f"/rooms/{room_id}/messages", json=payload, headers=headers)
    assert first.status_code == 201
    assert retry.status_code == 200
    assert retry.get_json()["duplicate"] is True
    assert retry.get_json()["id"] == first.get_json()["id"]
    history = client.get(f"/rooms/{room_id}/messages", headers=headers).get_json()
    assert len(history["messages"]) == 1


def test_websocket_auth_send_receive_and_reconnect_deduplication(client, websocket_url):
    register(client, "alice")
    headers = login(client, "alice")
    room_id = client.post("/rooms", json={"name": "general"}, headers=headers).get_json()["id"]
    token = headers["Authorization"].split(" ", 1)[1]

    with connect_websocket(f"{websocket_url}/ws/rooms/{room_id}") as ws:
        ws.send(json.dumps({"token": token}))
        assert json.loads(ws.receive())["type"] == "ready"
        event = {"type": "send", "body": "hello live", "client_message_id": "stable-1"}
        ws.send(json.dumps(event))
        delivered = json.loads(ws.receive())
        assert delivered["type"] == "message"
        assert delivered["message"]["body"] == "hello live"
        assert delivered["duplicate"] is False

    # Reconnect and retrying the same client message ID returns the persisted row.
    with connect_websocket(f"{websocket_url}/ws/rooms/{room_id}") as ws:
        ws.send(json.dumps({"token": token}))
        assert json.loads(ws.receive())["type"] == "ready"
        ws.send(json.dumps(event))
        replay = json.loads(ws.receive())
        assert replay["duplicate"] is True
        assert replay["message"]["id"] == delivered["message"]["id"]



def test_malformed_bearer_token_is_rejected(client):
    response = client.get(
        "/rooms",
        headers={"Authorization": "Bearer not-a-valid-token%%%"},
    )
    assert response.status_code == 401



def test_websocket_rejects_non_member(client, websocket_url):
    register(client, "owner")
    register(client, "outsider")
    owner_headers = login(client, "owner")
    outsider_token = login(client, "outsider")["Authorization"].split(" ", 1)[1]
    room_id = client.post("/rooms", json={"name": "private"}, headers=owner_headers).get_json()["id"]

    with connect_websocket(f"{websocket_url}/ws/rooms/{room_id}") as ws:
        ws.send(json.dumps({"token": outsider_token}))
        rejection = json.loads(ws.receive())
        assert rejection == {"type": "error", "error": "forbidden"}



def test_websocket_broadcast_reaches_other_room_members(client, websocket_url):
    register(client, "alice")
    bob_id = register(client, "bob")
    alice_headers = login(client, "alice")
    bob_headers = login(client, "bob")
    room_id = client.post("/rooms", json={"name": "general"}, headers=alice_headers).get_json()["id"]
    assert client.post(
        f"/rooms/{room_id}/members",
        json={"user_id": bob_id},
        headers=alice_headers,
    ).status_code == 200

    alice_token = alice_headers["Authorization"].split(" ", 1)[1]
    bob_token = bob_headers["Authorization"].split(" ", 1)[1]
    with connect_websocket(f"{websocket_url}/ws/rooms/{room_id}") as alice_ws:
        alice_ws.send(json.dumps({"token": alice_token}))
        assert json.loads(alice_ws.receive())["type"] == "ready"
        with connect_websocket(f"{websocket_url}/ws/rooms/{room_id}") as bob_ws:
            bob_ws.send(json.dumps({"token": bob_token}))
            assert json.loads(bob_ws.receive())["type"] == "ready"
            alice_ws.send(json.dumps({
                "type": "send",
                "body": "broadcast to the room",
                "client_message_id": "broadcast-1",
            }))
            alice_event = json.loads(alice_ws.receive())
            bob_event = json.loads(bob_ws.receive())

    assert alice_event == bob_event
    assert alice_event["type"] == "message"
    assert alice_event["message"]["body"] == "broadcast to the room"
    assert alice_event["message"]["sender_username"] == "alice"
