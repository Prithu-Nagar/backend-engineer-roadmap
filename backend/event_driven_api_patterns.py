"""
Day 67 — Event-Driven API Patterns

A small framework-neutral example showing how an API can persist an event
request and publish an event only after the transaction succeeds.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Event:
    event_id: str
    event_type: str
    aggregate_id: int
    payload: dict[str, object]


class EventPublisher(Protocol):
    def publish(self, event: Event) -> None:
        ...


class EventStore(Protocol):
    def save(self, event: Event) -> None:
        ...


class NotificationEventService:
    """Coordinates durable event creation with an explicit publication step."""

    def __init__(
        self,
        event_store: EventStore,
        publisher: EventPublisher,
    ) -> None:
        self._event_store = event_store
        self._publisher = publisher

    def create_event(
        self,
        event_id: str,
        event_type: str,
        aggregate_id: int,
        payload: dict[str, object],
    ) -> Event:
        if not event_id.strip():
            raise ValueError("event_id must not be empty")
        if not event_type.strip():
            raise ValueError("event_type must not be empty")
        if aggregate_id <= 0:
            raise ValueError("aggregate_id must be positive")

        event = Event(
            event_id=event_id,
            event_type=event_type,
            aggregate_id=aggregate_id,
            payload=dict(payload),
        )
        self._event_store.save(event)
        return event

    def publish_after_commit(self, event: Event) -> None:
        """Publish only after the owning transaction has successfully committed."""
        self._publisher.publish(event)


class InMemoryEventStore:
    def __init__(self) -> None:
        self.events: list[Event] = []

    def save(self, event: Event) -> None:
        self.events.append(event)


class RecordingPublisher:
    def __init__(self) -> None:
        self.published: list[Event] = []

    def publish(self, event: Event) -> None:
        self.published.append(event)


def main() -> None:
    store = InMemoryEventStore()
    publisher = RecordingPublisher()
    service = NotificationEventService(store, publisher)

    event = service.create_event(
        event_id="evt-1",
        event_type="notification.requested",
        aggregate_id=42,
        payload={"channel": "email", "recipient": "user@example.com"},
    )

    # In production, this call would happen through an outbox publisher after
    # the transaction containing event persistence has committed.
    service.publish_after_commit(event)

    print("stored:", store.events)
    print("published:", publisher.published)


if __name__ == "__main__":
    main()
