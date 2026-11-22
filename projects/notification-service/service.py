"""Application service and in-memory notification queue."""

from __future__ import annotations

from queue import Queue
from threading import RLock

from models import Notification, NotificationStatus


class NotificationNotFoundError(LookupError):
    """Raised when a notification identifier is unknown."""


class NotificationService:
    """Coordinates request validation, storage, and worker enqueueing.

    The in-memory store and queue are local-demo adapters, not durable
    production infrastructure. A process restart loses pending work.
    """

    ALLOWED_CHANNELS = frozenset({"email", "sms", "push"})

    def __init__(self) -> None:
        self._notifications: dict[str, Notification] = {}
        self._lock = RLock()
        self.queue: Queue[str] = Queue()

    def enqueue(self, *, recipient: str, channel: str, message: str) -> Notification:
        recipient = recipient.strip() if isinstance(recipient, str) else ""
        message = message.strip() if isinstance(message, str) else ""
        channel = channel.strip().lower() if isinstance(channel, str) else ""
        if not recipient:
            raise ValueError("recipient is required")
        if channel not in self.ALLOWED_CHANNELS:
            raise ValueError("channel must be email, sms, or push")
        if not message:
            raise ValueError("message is required")

        notification = Notification(
            recipient=recipient, channel=channel, message=message
        )
        with self._lock:
            notification.status = NotificationStatus.QUEUED
            self._notifications[notification.id] = notification
            self.queue.put(notification.id)
        return notification

    def get(self, notification_id: str) -> Notification:
        with self._lock:
            try:
                return self._notifications[notification_id]
            except KeyError as exc:
                raise NotificationNotFoundError(notification_id) from exc

    def mark_processing(self, notification_id: str) -> Notification:
        with self._lock:
            notification = self.get(notification_id)
            notification.status = NotificationStatus.PROCESSING
            notification.attempts += 1
            notification.error = None
            return notification

    def mark_sent(self, notification_id: str, provider_message_id: str) -> Notification:
        with self._lock:
            notification = self.get(notification_id)
            notification.status = NotificationStatus.SENT
            notification.provider_message_id = provider_message_id
            notification.error = None
            return notification

    def mark_failed(self, notification_id: str, error: str) -> Notification:
        with self._lock:
            notification = self.get(notification_id)
            notification.status = NotificationStatus.FAILED
            notification.error = error
            return notification
