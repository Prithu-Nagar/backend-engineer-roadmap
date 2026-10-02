"""
Day 63 — Observer and Adapter Design Patterns in Python

A backend-oriented example showing event notification through Observer and
integration of an incompatible external notifier through Adapter.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class NotificationEvent:
    notification_id: int
    recipient: str
    message: str


class NotificationObserver(Protocol):
    """Contract implemented by notification subscribers."""

    def update(self, event: NotificationEvent) -> None:
        ...


class NotificationSubject:
    """Publishes notification events to registered observers."""

    def __init__(self) -> None:
        self._observers: list[NotificationObserver] = []

    def subscribe(self, observer: NotificationObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: NotificationObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def publish(self, event: NotificationEvent) -> None:
        for observer in tuple(self._observers):
            observer.update(event)


class AuditObserver:
    def update(self, event: NotificationEvent) -> None:
        print(f"AUDIT notification={event.notification_id} recipient={event.recipient}")


class ExternalSmsClient:
    """Simulates an external client with a different method contract."""

    def send_text(self, phone_number: str, text: str) -> None:
        print(f"SMS {phone_number}: {text}")


class SmsAdapter:
    """Adapts the external SMS client's contract to NotificationObserver."""

    def __init__(self, client: ExternalSmsClient) -> None:
        self._client = client

    def update(self, event: NotificationEvent) -> None:
        self._client.send_text(event.recipient, event.message)


def main() -> None:
    subject = NotificationSubject()
    subject.subscribe(AuditObserver())
    subject.subscribe(SmsAdapter(ExternalSmsClient()))

    subject.publish(NotificationEvent(1, "+15550001", "Your task is ready."))


if __name__ == "__main__":
    main()
