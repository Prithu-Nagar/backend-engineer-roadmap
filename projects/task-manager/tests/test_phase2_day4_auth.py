"""Phase 2 Day 4 integration tests for authentication and task ownership."""

from typing import ClassVar

import pytest

from backend.app import create_app
from backend.extensions import db
from backend.models import User


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict[str, object]] = {}
    SECRET_KEY = "test-secret-key"
    JWT_SECRET = "test-jwt-secret-that-is-long-enough-for-tests"
    JWT_ACCESS_TOKEN_TTL_SECONDS = 900
    PASSWORD_MIN_LENGTH = 8


@pytest.fixture()
def app():
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, username="alice", email="alice@example.com", password="correct-horse"):
    return client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": password},
    )


def login(client, username="alice", password="correct-horse"):
    return client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )


def auth_headers(client, username="alice"):
    response = login(client, username=username)
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json['access_token']}"}


def test_register_persists_password_hash_and_never_returns_it(client, app):
    response = register(client)
    assert response.status_code == 201
    assert response.json["user"]["username"] == "alice"
    assert "password_hash" not in response.json["user"]

    with app.app_context():
        user = User.query.filter_by(username="alice").one()
        assert user.password_hash != "correct-horse"
        assert "pbkdf2" in user.password_hash


def test_registration_rejects_weak_password_and_duplicate_identity(client):
    weak = register(client, password="short")
    assert weak.status_code == 400
    assert register(client).status_code == 201
    assert register(client, username="alice2").status_code == 409


def test_public_registration_cannot_assign_admin_role(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "regular",
            "email": "regular@example.com",
            "password": "correct-horse",
            "role": "admin",
        },
    )
    assert response.status_code == 201
    assert response.json["user"]["role"] == "user"


def test_login_returns_bearer_token_and_me_resolves_identity(client):
    register(client)
    token_response = login(client)
    assert token_response.status_code == 200
    assert token_response.json["token_type"] == "Bearer"
    assert token_response.json["expires_in"] == 900

    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token_response.json['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json["user"]["email"] == "alice@example.com"


def test_login_rejects_invalid_password(client):
    register(client)
    response = login(client, password="wrong-password")
    assert response.status_code == 401
    assert response.json["error"]["code"] == "INVALID_CREDENTIALS"


@pytest.mark.parametrize("header", [None, "Bearer invalid.token", "Basic abc"])
def test_protected_endpoints_reject_missing_or_invalid_tokens(client, header):
    headers = {} if header is None else {"Authorization": header}
    response = client.get("/api/tasks/", headers=headers)
    assert response.status_code == 401


def test_user_can_create_and_list_only_own_tasks(client):
    register(client)
    headers = auth_headers(client)
    created = client.post(
        "/api/tasks/",
        json={"title": "My task"},
        headers=headers,
    )
    assert created.status_code == 201
    assert "user_id" not in created.json["task"]

    assert client.get("/api/tasks/", headers=headers).json["tasks"][0]["title"] == "My task"


def test_user_cannot_read_another_users_task(client, app):
    register(client)
    alice_headers = auth_headers(client)
    created = client.post(
        "/api/tasks/", json={"title": "Alice task"}, headers=alice_headers
    )
    task_id = created.json["task"]["id"]

    register(client, username="bob", email="bob@example.com")
    bob_headers = auth_headers(client, username="bob")

    response = client.get(f"/api/tasks/{task_id}", headers=bob_headers)
    assert response.status_code == 404
    assert response.json["error"]["code"] == "TASK_NOT_FOUND"
    assert client.get("/api/tasks/", headers=bob_headers).json["tasks"] == []


def test_admin_can_list_tasks_across_owners(client, app):
    register(client)
    alice_headers = auth_headers(client)
    client.post("/api/tasks/", json={"title": "Alice task"}, headers=alice_headers)

    with app.app_context():
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash="not-used-in-this-token-test",
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        admin_id = admin.id

    # Issue an admin token through the same application signing configuration.
    from datetime import UTC, datetime, timedelta

    import jwt

    with app.app_context():
        token = jwt.encode(
            {
                "sub": str(admin_id),
                "iat": datetime.now(UTC),
                "exp": datetime.now(UTC) + timedelta(minutes=5),
            },
            app.config["JWT_SECRET"],
            algorithm="HS256",
        )
    response = client.get(
        "/api/tasks/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert [task["title"] for task in response.json["tasks"]] == ["Alice task"]
