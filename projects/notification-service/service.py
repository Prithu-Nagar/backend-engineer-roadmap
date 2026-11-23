"""Application service and in-memory notification queue."""

from __future__ import annotations

from queue import Queue
from threading import RLock

from models import Notification, NotificationStatus


class NotificationNotFoundError(LookupError):
    """Raised when a notification identifier is unknown."""


class IdempotencyConflictError(ValueError):
    """Raised when a key is reused for a different notification payload."""


class NotificationService:
    """Coordinates validation, in-memory storage, deduplication, and enqueueing.

    The store and queue are local-demo adapters, not durable infrastructure.
    """

    ALLOWED_CHANNELS = frozenset({"email", "sms", "push"})

    def __init__(self) -> None:
        self._notifications: dict[str, Notification] = {}
        self._idempotency_index: dict[str, str] = {}
        self._lock = RLock()
        self.queue: Queue[str] = Queue()

    def enqueue(
        self, *, recipient: str, channel: str, message: str,
        idempotency_key: str | None = None,
    ) -> Notification:
        recipient = recipient.strip() if isinstance(recipient, str) else ""
        message = message.strip() if isinstance(message, str) else ""
        channel = channel.strip().lower() if isinstance(channel, str) else ""
        key = idempotency_key.strip() if isinstance(idempotency_key, str) else None
        if not recipient:
            raise ValueError("recipient is required")
        if channel not in self.ALLOWED_CHANNELS:
            raise ValueError("channel must be email, sms, or push")
        if not message:
            raise ValueError("message is required")
        if idempotency_key is not None and not key:
            raise ValueError("idempotency_key must not be empty")

        with self._lock:
            if key and key in self._idempotency_index:
                existing = self._notifications[self._idempotency_index[key]]
                if (existing.recipient, existing.channel, existing.message) != (recipient, channel, message):
                    raise IdempotencyConflictError("idempotency key was already used for a different request")
                return existing

            notification = Notification(
                recipient=recipient, channel=channel, message=message,
                idempotency_key=key,
            )
            notification.status = NotificationStatus.QUEUED
            self._notifications[notification.id] = notification
            if key:
                self._idempotency_index[key] = notification.id
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
            notification.next_retry_delay = None
            return notification

    def mark_retrying(self, notification_id: str, error: str, delay: float) -> Notification:
        with self._lock:
            notification = self.get(notification_id)
            notification.status = NotificationStatus.RETRYING
            notification.error = error
            notification.next_retry_delay = delay
            return notification

    def requeue(self, notification_id: str) -> None:
        with self._lock:
            notification = self.get(notification_id)
            notification.status = NotificationStatus.QUEUED
            self.queue.put(notification_id)

    def mark_sent(self, notification_id: str, provider_message_id: str) -> Notification:
        with self._lock:
            notification = self.get(notification_id)
            notification.status = NotificationStatus.SENT
            notification.provider_message_id = provider_message_id
            notification.error = None
            notification.next_retry_delay = None
            return notification

    def mark_failed(self, notification_id: str, error: str) -> Notification:
        with self._lock:
            notification = self.get(notification_id)
            notification.status = NotificationStatus.FAILED
            notification.error = error
            notification.next_retry_delay = None
            return notification
