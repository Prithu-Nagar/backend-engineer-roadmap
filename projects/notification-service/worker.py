"""Synchronous worker abstraction for queued notification requests."""

from __future__ import annotations

from queue import Empty

from providers import NotificationProvider
from service import NotificationService


class NotificationWorker:
    """Consumes one queued notification and delegates delivery to a provider."""

    def __init__(
        self, service: NotificationService, provider: NotificationProvider
    ) -> None:
        self.service = service
        self.provider = provider

    def process_one(self, *, block: bool = False, timeout: float | None = None) -> bool:
        try:
            notification_id = self.service.queue.get(block=block, timeout=timeout)
        except Empty:
            return False

        try:
            notification = self.service.mark_processing(notification_id)
            try:
                provider_message_id = self.provider.send(
                    recipient=notification.recipient,
                    channel=notification.channel,
                    message=notification.message,
                )
            except Exception as exc:  # noqa: BLE001
                self.service.mark_failed(notification_id, str(exc) or exc.__class__.__name__)
            else:
                self.service.mark_sent(notification_id, provider_message_id)
        finally:
            self.service.queue.task_done()
        return True

    def run_until_empty(self) -> int:
        """Process currently queued work; return the number of consumed items."""
        processed = 0
        while self.process_one():
            processed += 1
        return processed
