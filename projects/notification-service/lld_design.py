"""
Day 63 — Notification Service LLD

A small LLD artifact combining Observer and Adapter around a notification
service. The core workflow depends on stable contracts while provider-specific
integration remains at the edge.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Notification:
    notification_id: int
    recipient: str
    message: str


class NotificationObserver(Protocol):
    def update(self, notification: Notification) -> None:
        ...


class NotificationSubject:
    def __init__(self) -> None:
        self._observers: list[NotificationObserver] = []

    def subscribe(self, observer: NotificationObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def publish(self, notification: Notification) -> None:
        for observer in tuple(self._observers):
            observer.update(notification)


class AuditObserver:
    def __init__(self) -> None:
        self.events: list[int] = []

    def update(self, notification: Notification) -> None:
        self.events.append(notification.notification_id)


class EmailProvider:
    """External provider with an interface owned outside the application."""

    def send_message(self, address: str, content: str) -> None:
        print(f"EMAIL {address}: {content}")


class EmailAdapter:
    """Translates the provider contract into the observer contract."""

    def __init__(self, provider: EmailProvider) -> None:
        self._provider = provider

    def update(self, notification: Notification) -> None:
        self._provider.send_message(
            notification.recipient,
            notification.message,
        )


class NotificationService:
    def __init__(self, subject: NotificationSubject) -> None:
        self._subject = subject

    def notify(self, notification: Notification) -> None:
        if notification.notification_id <= 0:
            raise ValueError("notification_id must be positive")
        if not notification.recipient.strip():
            raise ValueError("recipient must not be empty")
        if not notification.message.strip():
            raise ValueError("message must not be empty")
        self._subject.publish(notification)


def main() -> None:
    subject = NotificationSubject()
    audit = AuditObserver()
    subject.subscribe(audit)
    subject.subscribe(EmailAdapter(EmailProvider()))

    service = NotificationService(subject)
    service.notify(Notification(1, "user@example.com", "Your task is ready."))

    print(f"Audited notification IDs: {audit.events}")


if __name__ == "__main__":
    main()
