"""
Day 56 — Agent Backend Service

Provider-neutral backend service that coordinates an agent workflow while
keeping authentication, session persistence, tool execution, and model
integration behind explicit boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class AgentRequest:
    session_id: str
    user_id: int
    message: str


@dataclass
class AgentResponse:
    session_id: str
    answer: str
    tool_results: list[dict[str, Any]] = field(default_factory=list)


class SessionStore(Protocol):
    async def load(self, session_id: str) -> list[dict[str, Any]]: ...

    async def append(self, session_id: str, message: dict[str, Any]) -> None: ...


class AgentRuntime(Protocol):
    async def run(
        self,
        history: list[dict[str, Any]],
        message: str,
    ) -> tuple[str, list[dict[str, Any]]]: ...


class InMemorySessionStore:
    def __init__(self) -> None:
        self.sessions: dict[str, list[dict[str, Any]]] = {}

    async def load(self, session_id: str) -> list[dict[str, Any]]:
        return list(self.sessions.get(session_id, []))

    async def append(self, session_id: str, message: dict[str, Any]) -> None:
        self.sessions.setdefault(session_id, []).append(message)


class DemoAgentRuntime:
    async def run(
        self,
        history: list[dict[str, Any]],
        message: str,
    ) -> tuple[str, list[dict[str, Any]]]:
        del history
        return (
            f"Processed request: {message}",
            [],
        )


class AgentBackendService:
    def __init__(
        self,
        session_store: SessionStore,
        runtime: AgentRuntime,
    ) -> None:
        self.session_store = session_store
        self.runtime = runtime

    async def handle(self, request: AgentRequest) -> AgentResponse:
        message = request.message.strip()
        if not message:
            raise ValueError("message must not be empty")

        history = await self.session_store.load(request.session_id)

        await self.session_store.append(
            request.session_id,
            {
                "role": "user",
                "user_id": request.user_id,
                "content": message,
            },
        )

        answer, tool_results = await self.runtime.run(history, message)

        await self.session_store.append(
            request.session_id,
            {
                "role": "assistant",
                "content": answer,
            },
        )

        return AgentResponse(
            session_id=request.session_id,
            answer=answer,
            tool_results=tool_results,
        )
