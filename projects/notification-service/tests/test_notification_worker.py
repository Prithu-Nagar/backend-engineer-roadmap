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
    worker = NotificationWorker(service, FailingProvider(), max_attempts=1)

    assert worker.process_one()
    result = service.get(notification.id)
    assert result.status is NotificationStatus.FAILED
    assert result.error == "provider unavailable"
    assert result.attempts == 1
    assert service.queue.unfinished_tasks == 0


def test_worker_returns_false_when_queue_is_empty(service):
    assert NotificationWorker(service, LocalNotificationProvider()).process_one() is False


def test_transient_failure_retries_with_exponential_backoff_and_succeeds(service):
    class FlakyProvider:
        calls = 0

        def send(self, **kwargs):
            self.calls += 1
            if self.calls < 3:
                raise ConnectionError("temporary outage")
            return "provider-3"

    delays = []
    notification = service.enqueue(recipient="user", channel="email", message="Hello")
    worker = NotificationWorker(
        service, FlakyProvider(), max_attempts=3, base_delay=0.25,
        sleeper=delays.append,
    )

    assert worker.run_until_empty() == 3
    result = service.get(notification.id)
    assert result.status is NotificationStatus.SENT
    assert result.attempts == 3
    assert result.provider_message_id == "provider-3"
    assert delays == [0.25, 0.5]
    assert service.queue.unfinished_tasks == 0


def test_retry_exhaustion_marks_notification_failed(service):
    delays = []
    notification = service.enqueue(recipient="user", channel="sms", message="Code")
    worker = NotificationWorker(
        service, FailingProvider(), max_attempts=2, base_delay=0.1,
        sleeper=delays.append,
    )

    assert worker.run_until_empty() == 2
    result = service.get(notification.id)
    assert result.status is NotificationStatus.FAILED
    assert result.attempts == 2
    assert result.error == "provider unavailable"
    assert result.next_retry_delay is None
    assert delays == [0.1]
    assert service.queue.unfinished_tasks == 0


def test_permanent_provider_failure_is_not_retried(service):
    class PermanentFailure:
        def send(self, **kwargs):
            raise ValueError("invalid recipient")

    notification = service.enqueue(recipient="bad", channel="email", message="Hello")
    worker = NotificationWorker(service, PermanentFailure(), sleeper=lambda _: pytest.fail("unexpected retry"))

    assert worker.process_one()
    result = service.get(notification.id)
    assert result.status is NotificationStatus.FAILED
    assert result.attempts == 1


def test_idempotency_key_returns_existing_notification_without_duplicate_enqueue(service):
    first = service.enqueue(
        recipient="user", channel="email", message="Hello", idempotency_key="request-1"
    )
    duplicate = service.enqueue(
        recipient="user", channel="email", message="Hello", idempotency_key="request-1"
    )

    assert duplicate.id == first.id
    assert service.queue.qsize() == 1


def test_reusing_idempotency_key_with_different_payload_is_rejected(service):
    from service import IdempotencyConflictError

    service.enqueue(
        recipient="user", channel="email", message="Hello", idempotency_key="request-1"
    )
    with pytest.raises(IdempotencyConflictError):
        service.enqueue(
            recipient="other", channel="email", message="Hello", idempotency_key="request-1"
        )
    assert service.queue.qsize() == 1
