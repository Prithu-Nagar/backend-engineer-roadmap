"""
Day 55 — Tool Execution Patterns

Provider-neutral patterns for registering, validating, and executing tools
requested by an agent. The model can request an action, but the application
owns validation, authorization, and execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


ToolFunction = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    handler: ToolFunction


class ToolRegistry:
    """Register a bounded set of application-controlled tools."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if not tool.name.strip():
            raise ValueError("tool name must not be empty")
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        *,
        allowed_tools: set[str] | None = None,
    ) -> dict[str, Any]:
        if allowed_tools is not None and tool_name not in allowed_tools:
            raise PermissionError(f"tool is not allowed: {tool_name}")

        tool = self._tools.get(tool_name)
        if tool is None:
            raise KeyError(f"unknown tool: {tool_name}")

        if not isinstance(arguments, dict):
            raise TypeError("tool arguments must be a dictionary")

        return tool.handler(**arguments)


def get_task(*, task_id: int) -> dict[str, Any]:
    """Example read-only application tool."""
    if task_id <= 0:
        raise ValueError("task_id must be positive")

    return {"task_id": task_id, "status": "pending"}


def main() -> None:
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="get_task",
            description="Retrieve a task by its identifier.",
            handler=get_task,
        )
    )

    result = registry.execute(
        "get_task",
        {"task_id": 42},
        allowed_tools={"get_task"},
    )
    print(result)


if __name__ == "__main__":
    main()
