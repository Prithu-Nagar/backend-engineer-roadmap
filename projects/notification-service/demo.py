"""Deterministic end-to-end demo of enqueue, retry, and delivery status."""

from providers import LocalNotificationProvider
from service import NotificationService
from worker import NotificationWorker


class FlakyLocalProvider(LocalNotificationProvider):
    """Simulate one transient outage before delegating to local delivery."""

    def __init__(self) -> None:
        super().__init__()
        self.failed_once = False

    def send(self, *, recipient: str, channel: str, message: str) -> str:
        if not self.failed_once:
            self.failed_once = True
            raise ConnectionError("simulated temporary provider outage")
        return super().send(recipient=recipient, channel=channel, message=message)


def main() -> None:
    service = NotificationService()
    provider = FlakyLocalProvider()
    worker = NotificationWorker(
        service,
        provider,
        max_attempts=3,
        base_delay=0,
        sleeper=lambda _: None,
    )

    request = {
        "recipient": "demo@example.com",
        "channel": "email",
        "message": "Your task is complete.",
    }
    notification = service.enqueue(**request, idempotency_key="demo-request-1")
    duplicate = service.enqueue(**request, idempotency_key="demo-request-1")

    print(f"Enqueued: {notification.id} ({notification.status.value})")
    print(f"Duplicate request reused original: {duplicate.id == notification.id}")
    print(f"Worker attempts processed: {worker.run_until_empty()}")

    result = service.get(notification.id)
    print(f"Final status: {result.status.value}")
    print(f"Attempts: {result.attempts}")
    print(f"Provider message ID: {result.provider_message_id}")
    print(f"Local deliveries: {len(provider.deliveries)}")


if __name__ == "__main__":
    main()
