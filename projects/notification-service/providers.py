"""Provider boundary and deterministic local delivery adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class NotificationProvider(Protocol):
    def send(self, *, recipient: str, channel: str, message: str) -> str:
        """Deliver a message and return the provider's message identifier."""


@dataclass(frozen=True)
class LocalDelivery:
    recipient: str
    channel: str
    message: str
    provider_message_id: str


class LocalNotificationProvider:
    """Local demo provider; records deliveries without contacting external services."""

    def __init__(self) -> None:
        self.deliveries: list[LocalDelivery] = []

    def send(self, *, recipient: str, channel: str, message: str) -> str:
        provider_message_id = f"local-{len(self.deliveries) + 1}"
        self.deliveries.append(
            LocalDelivery(recipient, channel, message, provider_message_id)
        )
        return provider_message_id
