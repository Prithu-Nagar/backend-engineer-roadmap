"""API, enqueue, worker, and local-provider behavior tests."""

import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

pytest.importorskip("flask")

from app import create_app
from models import NotificationStatus
from service import NotificationService


@pytest.fixture
def service():
    return NotificationService()


@pytest.fixture
def app(service):
    application = create_app(service=service)
    application.config.update(TESTING=True)
    return application


def test_create_notification_enqueues_and_returns_accepted(app, service):
    response = app.test_client().post(
        "/notifications",
        json={"recipient": "person@example.com", "channel": "email", "message": "Hello"},
    )

    assert response.status_code == 202
    body = response.get_json()
    assert body["status"] == NotificationStatus.QUEUED.value
    assert service.queue.qsize() == 1
    assert app.test_client().get(f"/notifications/{body['id']}").status_code == 200


@pytest.mark.parametrize(
    "payload",
    [
        {"recipient": "", "channel": "email", "message": "Hello"},
        {"recipient": "user", "channel": "fax", "message": "Hello"},
        {"recipient": "user", "channel": "email", "message": ""},
    ],
)
def test_invalid_notification_is_rejected(app, payload):
    response = app.test_client().post("/notifications", json=payload)
    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid_notification"


def test_non_object_json_is_rejected(app):
    assert app.test_client().post("/notifications", json=["not", "an", "object"]).status_code == 400


def test_unknown_notification_returns_404(app):
    response = app.test_client().get("/notifications/missing")
    assert response.status_code == 404


