"""Notification domain model and delivery states."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class NotificationStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    PROCESSING = "processing"
    SENT = "sent"
    FAILED = "failed"


@dataclass
class Notification:
    """A single-channel notification request."""

    recipient: str
    channel: str
    message: str
    id: str = field(default_factory=lambda: uuid4().hex)
    status: NotificationStatus = NotificationStatus.CREATED
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    attempts: int = 0
    provider_message_id: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "recipient": self.recipient,
            "channel": self.channel,
            "message": self.message,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "attempts": self.attempts,
            "provider_message_id": self.provider_message_id,
            "error": self.error,
        }
