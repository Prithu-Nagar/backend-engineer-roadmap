"""Integration tests for authenticated users, follows, and persistent posts."""
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
        "DATABASE": str(tmp_path / "news_feed.sqlite3"),
        "SECRET_KEY": "test-secret",
    })
    return app.test_client()


def register(client, username):
    response = client.post(
        "/auth/register", json={"username": username, "password": "correct-horse"}
    )
    assert response.status_code == 201
    return response.get_json()["id"]


def login(client, username):
    response = client.post(
        "/auth/login", json={"username": username, "password": "correct-horse"}
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.get_json()['access_token']}"}


def test_users_follow_relationship_and_profile(client):
    alice_id = register(client, "alice")
    bob_id = register(client, "bob")
    alice = login(client, "alice")
    bob = login(client, "bob")

    assert client.get("/users", headers=alice).status_code == 200
    assert client.post(f"/users/{alice_id}/follow", headers=alice).status_code == 400
    assert client.post("/users/999/follow", headers=alice).status_code == 404
    assert client.post(f"/users/{bob_id}/follow", headers=alice).status_code == 200
    assert client.post(f"/users/{bob_id}/follow", headers=alice).status_code == 200
    profile = client.get(f"/users/{bob_id}", headers=alice).get_json()
    assert profile["followers_count"] == 1
    assert profile["is_following"] is True
    assert client.get(f"/users/{bob_id}/followers", headers=bob).get_json()["users"][0]["id"] == alice_id
    assert client.get(f"/users/{alice_id}/following", headers=alice).get_json()["users"][0]["id"] == bob_id
    assert client.delete(f"/users/{bob_id}/follow", headers=alice).status_code == 200
    assert client.get(f"/users/{bob_id}", headers=alice).get_json()["followers_count"] == 0


def test_profile_update_and_validation(client):
    user_id = register(client, "alice")
    headers = login(client, "alice")
    assert client.patch("/users/me", json={"bio": "Backend engineer"}, headers=headers).status_code == 200
    assert client.get(f"/users/{user_id}", headers=headers).get_json()["bio"] == "Backend engineer"
    assert client.patch("/users/me", json={"bio": "x" * 281}, headers=headers).status_code == 400
    assert client.post("/posts", json={"body": " "}, headers=headers).status_code == 400


def test_post_creation_retrieval_and_persistence(client):
    alice_id = register(client, "alice")
    bob_id = register(client, "bob")
    alice = login(client, "alice")
    bob = login(client, "bob")

    created = client.post("/posts", json={"body": "from bob"}, headers=bob)
    assert created.status_code == 201
    post_id = created.get_json()["id"]
    assert created.get_json()["author_id"] == bob_id
    assert client.get(f"/posts/{post_id}", headers=alice).get_json()["body"] == "from bob"
    assert client.get("/posts/999", headers=alice).status_code == 404
    assert client.post("/posts", json={"body": "x" * 2001}, headers=alice).status_code == 400
    assert alice_id != bob_id


def test_authentication_duplicate_user_and_persistence(client):
    register(client, "alice")
    assert client.post(
        "/auth/register", json={"username": "ALICE", "password": "correct-horse"}
    ).status_code == 409
    assert client.get("/users").status_code == 401
    headers = login(client, "alice")
    created = client.post("/posts", json={"body": "persistent"}, headers=headers)

    reopened = create_app({
        "TESTING": True,
        "DATABASE": client.application.config["DATABASE"],
        "SECRET_KEY": "test-secret",
    }).test_client()
    post_id = created.get_json()["id"]
    assert reopened.get(f"/posts/{post_id}", headers=headers).get_json()["body"] == "persistent"
    assert reopened.get(f"/posts/{post_id}", headers={"Authorization": "Bearer invalid"}).status_code == 401
