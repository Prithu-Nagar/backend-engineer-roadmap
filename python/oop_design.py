"""
Day 20 — OOP Design

Topics:
- Abstract interfaces
- Abstract Base Classes
- Dependency Inversion
- Dependency Injection
- Composition

The example demonstrates a notification system where the high-level
service depends on an abstraction instead of a concrete implementation.
"""

from abc import ABC, abstractmethod


class MessageSender(ABC):
    """Abstract interface for message delivery."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        """Send a message to a recipient."""
        raise NotImplementedError


class EmailSender(MessageSender):
    """Concrete email implementation."""

    def send(self, recipient: str, message: str) -> None:
        print(f"Email sent to {recipient}: {message}")


class ConsoleSender(MessageSender):
    """Simple implementation useful for local testing."""

    def send(self, recipient: str, message: str) -> None:
        print(f"Console message to {recipient}: {message}")


class NotificationService:
    """
    High-level service depending on the MessageSender abstraction.

    The concrete implementation is injected through the constructor.
    """

    def __init__(self, sender: MessageSender) -> None:
        self.sender = sender

    def notify(self, recipient: str, message: str) -> None:
        self.sender.send(recipient, message)


def main() -> None:
    email_service = NotificationService(EmailSender())
    email_service.notify(
        "developer@example.com",
        "Task created successfully.",
    )

    console_service = NotificationService(ConsoleSender())
    console_service.notify(
        "local-user",
        "Task completed successfully.",
    )


if __name__ == "__main__":
    main()