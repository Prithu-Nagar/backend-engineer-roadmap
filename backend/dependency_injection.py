"""
Day 63 — Dependency Injection for Backend Services

A framework-neutral example showing constructor injection, explicit
composition, and replaceable infrastructure dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Notification:
    notification_id: int
    recipient: str
    message: str


class NotificationRepository(Protocol):
    def save(self, notification: Notification) -> Notification:
        ...

    def get(self, notification_id: int) -> Notification | None:
        ...


class NotificationSender(Protocol):
    def send(self, notification: Notification) -> None:
        ...


class InMemoryNotificationRepository:
    def __init__(self) -> None:
        self._items: dict[int, Notification] = {}

    def save(self, notification: Notification) -> Notification:
        self._items[notification.notification_id] = notification
        return notification

    def get(self, notification_id: int) -> Notification | None:
        return self._items.get(notification_id)


class ConsoleNotificationSender:
    def send(self, notification: Notification) -> None:
        print(f"NOTIFY {notification.recipient}: {notification.message}")


class NotificationService:
    """Application service whose dependencies are injected at construction."""

    def __init__(
        self,
        repository: NotificationRepository,
        sender: NotificationSender,
    ) -> None:
        self._repository = repository
        self._sender = sender

    def create_and_send(
        self,
        *,
        notification_id: int,
        recipient: str,
        message: str,
    ) -> Notification:
        if notification_id <= 0:
            raise ValueError("notification_id must be positive")
        if not recipient.strip():
            raise ValueError("recipient must not be empty")
        if not message.strip():
            raise ValueError("message must not be empty")

        notification = Notification(
            notification_id=notification_id,
            recipient=recipient.strip(),
            message=message.strip(),
        )
        saved = self._repository.save(notification)
        self._sender.send(saved)
        return saved


def build_application() -> NotificationService:
    repository = InMemoryNotificationRepository()
    sender = ConsoleNotificationSender()
    return NotificationService(repository, sender)


if __name__ == "__main__":
    service = build_application()
    print(service.create_and_send(
        notification_id=1,
        recipient="user@example.com",
        message="Your report is ready.",
    ))
