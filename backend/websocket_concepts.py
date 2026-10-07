"""Framework-neutral WebSocket concepts for a chat backend.

The example models connection ownership and message fan-out without coupling
the learning artifact to a particular WebSocket framework.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Protocol


class Connection(Protocol):
    """Minimal connection contract required by the connection manager."""

    async def send(self, message: str) -> None:
        """Send a message to the connected client."""


@dataclass
class ConnectionManager:
    """Track connections by chat room and broadcast messages."""

    rooms: dict[str, set[Connection]] = field(
        default_factory=lambda: defaultdict(set)
    )

    def connect(self, room_id: str, connection: Connection) -> None:
        """Register a connection in a room."""
        self.rooms[room_id].add(connection)

    def disconnect(self, room_id: str, connection: Connection) -> None:
        """Remove a connection and clean up an empty room."""
        room = self.rooms.get(room_id)
        if room is None:
            return
        room.discard(connection)
        if not room:
            self.rooms.pop(room_id, None)

    async def broadcast(self, room_id: str, message: str) -> None:
        """Broadcast a message while isolating connection-level send failures."""
        connections = tuple(self.rooms.get(room_id, set()))
        for connection in connections:
            try:
                await connection.send(message)
            except (ConnectionError, OSError, RuntimeError):
                self.disconnect(room_id, connection)


@dataclass(frozen=True)
class ChatMessage:
    """Application-level message before persistence and fan-out."""

    room_id: str
    sender_id: int
    body: str


async def handle_message(
    manager: ConnectionManager,
    message: ChatMessage,
) -> None:
    """Fan out a validated message to the current room."""
    await manager.broadcast(message.room_id, message.body)
