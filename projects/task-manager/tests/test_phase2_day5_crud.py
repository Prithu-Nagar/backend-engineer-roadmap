"""Phase 2 Day 5 integration tests for task CRUD, filtering and pagination."""

from typing import ClassVar

import pytest

from backend.app import create_app
from backend.extensions import db


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
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def register_and_login(client, username="alice"):
    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "correct-horse",
        },
    )
    assert response.status_code == 201
    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": "correct-horse"},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json['access_token']}"}


def create_task(client, headers, title, **fields):
    return client.post(
        "/api/tasks/",
        json={"title": title, **fields},
        headers=headers,
    )


def test_task_crud_lifecycle(client):
    headers = register_and_login(client)

    created = create_task(
        client,
        headers,
        "Prepare release",
        description="Write release notes",
        priority="high",
    )
    assert created.status_code == 201
    task_id = created.json["task"]["id"]
    assert created.json["task"]["status"] == "pending"

    retrieved = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert retrieved.status_code == 200
    assert retrieved.json["task"]["title"] == "Prepare release"

    updated = client.patch(
        f"/api/tasks/{task_id}",
        json={"status": "completed", "title": "Release prepared"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json["task"]["status"] == "completed"
    assert updated.json["task"]["title"] == "Release prepared"

    deleted = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/api/tasks/{task_id}", headers=headers).status_code == 404


def test_list_filters_search_and_pagination(client):
    headers = register_and_login(client)
    create_task(client, headers, "Alpha task", status="pending", priority="high")
    create_task(client, headers, "Beta task", status="completed", priority="low")
    create_task(client, headers, "Another alpha", status="pending", priority="medium")

    response = client.get(
        "/api/tasks/?status=pending&search=alpha&page=1&per_page=1",
        headers=headers,
    )
    assert response.status_code == 200
    assert len(response.json["tasks"]) == 1
    assert response.json["pagination"] == {
        "page": 1,
        "per_page": 1,
        "total": 2,
        "pages": 2,
        "has_next": True,
        "has_previous": False,
    }

    second_page = client.get(
        "/api/tasks/?status=pending&search=alpha&page=2&per_page=1",
        headers=headers,
    )
    assert second_page.status_code == 200
    assert second_page.json["pagination"]["has_previous"] is True
    assert second_page.json["pagination"]["has_next"] is False


@pytest.mark.parametrize(
    ("query", "message"),
    [
        ("page=0", "Page must be at least 1."),
        ("per_page=101", "per_page must be between 1 and 100."),
        ("page=abc", "Page and per_page must be integers."),
        ("status=unknown", "Unsupported status filter."),
        ("sort_by=password", "Unsupported sort_by field."),
        ("sort_order=sideways", "sort_order must be 'asc' or 'desc'."),
    ],
)
def test_invalid_list_parameters_use_standard_error(client, query, message):
    headers = register_and_login(client)
    response = client.get(f"/api/tasks/?{query}", headers=headers)
    assert response.status_code == 422
    assert response.json["error"]["code"] == "VALIDATION_ERROR"
    assert response.json["error"]["message"] == message


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": " "},
        {"title": "x" * 201},
        {"title": "Valid", "status": "unknown"},
        {"title": "Valid", "priority": "urgent"},
        {"title": "Valid", "user_id": 999},
        {"title": "Valid", "description": 42},
    ],
)
def test_invalid_task_payload_is_rejected(client, payload):
    headers = register_and_login(client)
    response = client.post("/api/tasks/", json=payload, headers=headers)
    assert response.status_code == 422
    assert response.json["error"]["code"] == "VALIDATION_ERROR"


def test_update_rejects_empty_and_invalid_payload(client):
    headers = register_and_login(client)
    task_id = create_task(client, headers, "Existing").json["task"]["id"]

    empty = client.patch(f"/api/tasks/{task_id}", json={}, headers=headers)
    invalid = client.patch(
        f"/api/tasks/{task_id}",
        json={"priority": "critical"},
        headers=headers,
    )
    assert empty.status_code == 422
    assert invalid.status_code == 422


def test_user_cannot_update_or_delete_another_users_task(client):
    alice_headers = register_and_login(client, "alice")
    task_id = create_task(client, alice_headers, "Private task").json["task"]["id"]
    bob_headers = register_and_login(client, "bob")

    update = client.patch(
        f"/api/tasks/{task_id}",
        json={"title": "Hijacked"},
        headers=bob_headers,
    )
    delete = client.delete(f"/api/tasks/{task_id}", headers=bob_headers)
    assert update.status_code == 404
    assert delete.status_code == 404

    still_exists = client.get(f"/api/tasks/{task_id}", headers=alice_headers)
    assert still_exists.status_code == 200
    assert still_exists.json["task"]["title"] == "Private task"


def test_unauthenticated_crud_endpoints_are_rejected(client):
    assert client.get("/api/tasks/").status_code == 401
    assert client.post("/api/tasks/", json={"title": "Task"}).status_code == 401
    assert client.patch("/api/tasks/1", json={"title": "Task"}).status_code == 401
    assert client.delete("/api/tasks/1").status_code == 401
