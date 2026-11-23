"""Worker with bounded exponential retry for transient provider failures."""

from __future__ import annotations

from collections.abc import Callable
from queue import Empty
from time import sleep

from providers import NotificationProvider
from service import NotificationService


class NotificationWorker:
    """Consumes queued requests and retries transient failures up to a limit."""

    def __init__(
        self, service: NotificationService, provider: NotificationProvider,
        *, max_attempts: int = 3, base_delay: float = 1.0,
        sleeper: Callable[[float], None] = sleep,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if base_delay < 0:
            raise ValueError("base_delay must not be negative")
        self.service = service
        self.provider = provider
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.sleeper = sleeper

    def process_one(self, *, block: bool = False, timeout: float | None = None) -> bool:
        try:
            notification_id = self.service.queue.get(block=block, timeout=timeout)
        except Empty:
            return False

        retry_delay: float | None = None
        try:
            notification = self.service.mark_processing(notification_id)
            try:
                provider_message_id = self.provider.send(
                    recipient=notification.recipient,
                    channel=notification.channel,
                    message=notification.message,
                )
            except (ConnectionError, TimeoutError) as exc:
                error = str(exc) or exc.__class__.__name__
                if notification.attempts < self.max_attempts:
                    retry_delay = self.base_delay * (2 ** (notification.attempts - 1))
                    self.service.mark_retrying(notification_id, error, retry_delay)
                else:
                    self.service.mark_failed(notification_id, error)
            except Exception as exc:  # noqa: BLE001 - permanent provider failure
                self.service.mark_failed(notification_id, str(exc) or exc.__class__.__name__)
            else:
                self.service.mark_sent(notification_id, provider_message_id)
        finally:
            self.service.queue.task_done()

        if retry_delay is not None:
            self.sleeper(retry_delay)
            self.service.requeue(notification_id)
        return True

    def run_until_empty(self) -> int:
        """Process all currently queued work, including bounded retries."""
        processed = 0
        while self.process_one():
            processed += 1
        return processed
