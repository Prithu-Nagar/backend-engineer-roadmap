"""
Day 56 — Async Agent / Tool Orchestration

Provider-neutral example of coordinating asynchronous tool calls inside a
bounded agent workflow.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable


ToolHandler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


class AsyncToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolHandler] = {}

    def register(self, name: str, handler: ToolHandler) -> None:
        if not name.strip():
            raise ValueError("tool name must not be empty")
        self._tools[name] = handler

    async def execute(self, call: ToolCall) -> dict[str, Any]:
        handler = self._tools.get(call.name)
        if handler is None:
            raise KeyError(f"unknown tool: {call.name}")
        return await handler(call.arguments)


class AgentOrchestrator:
    def __init__(
        self,
        registry: AsyncToolRegistry,
        max_iterations: int = 5,
    ) -> None:
        if max_iterations <= 0:
            raise ValueError("max_iterations must be positive")

        self.registry = registry
        self.max_iterations = max_iterations

    async def run(self, calls: list[ToolCall]) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        for index in range(0, len(calls), 2):
            if index // 2 >= self.max_iterations:
                raise RuntimeError("agent iteration limit reached")

            batch = calls[index : index + 2]
            batch_results = await asyncio.gather(
                *(self.registry.execute(call) for call in batch),
                return_exceptions=True,
            )

            for call, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    results.append(
                        {
                            "tool": call.name,
                            "status": "failed",
                            "error": str(result),
                        }
                    )
                else:
                    results.append(
                        {
                            "tool": call.name,
                            "status": "succeeded",
                            "result": result,
                        }
                    )

        return results


async def get_user_profile(arguments: dict[str, Any]) -> dict[str, Any]:
    await asyncio.sleep(0)
    return {"user_id": arguments["user_id"], "name": "demo-user"}


async def calculate_total(arguments: dict[str, Any]) -> dict[str, Any]:
    await asyncio.sleep(0)
    return {"total": sum(arguments["values"])}


async def main() -> None:
    registry = AsyncToolRegistry()
    registry.register("get_user_profile", get_user_profile)
    registry.register("calculate_total", calculate_total)

    orchestrator = AgentOrchestrator(registry)

    results = await orchestrator.run(
        [
            ToolCall("get_user_profile", {"user_id": "u-100"}),
            ToolCall("calculate_total", {"values": [10, 20, 30]}),
        ]
    )

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
