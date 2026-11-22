"""Framework-independent notification service and worker tests."""

import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from models import NotificationStatus
from providers import LocalNotificationProvider
from service import NotificationService
from worker import NotificationWorker


@pytest.fixture
def service():
    return NotificationService()


def test_worker_delivers_through_local_provider(service):
    notification = service.enqueue(
        recipient="user@example.com", channel="email", message="Welcome"
    )
    provider = LocalNotificationProvider()
    worker = NotificationWorker(service, provider)

    assert worker.process_one()
    assert service.get(notification.id).status is NotificationStatus.SENT
    assert service.get(notification.id).provider_message_id == "local-1"
    assert provider.deliveries[0].message == "Welcome"
    assert service.queue.unfinished_tasks == 0


class FailingProvider:
    def send(self, **kwargs):
        raise ConnectionError("provider unavailable")


def test_worker_records_provider_failure_without_losing_queue_task(service):
    notification = service.enqueue(
        recipient="user", channel="sms", message="Code 123"
    )
    worker = NotificationWorker(service, FailingProvider())

    assert worker.process_one()
    result = service.get(notification.id)
    assert result.status is NotificationStatus.FAILED
    assert result.error == "provider unavailable"
    assert result.attempts == 1
    assert service.queue.unfinished_tasks == 0


def test_worker_returns_false_when_queue_is_empty(service):
    assert NotificationWorker(service, LocalNotificationProvider()).process_one() is False
