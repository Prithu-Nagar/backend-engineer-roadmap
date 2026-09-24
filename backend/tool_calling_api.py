"""
Day 55 — Tool-Calling API Patterns

Provider-neutral Flask-style API boundaries for agent tool calls.

The API accepts a structured tool request, validates the request, and delegates
execution to an application-owned registry. It does not allow the model or
client to execute arbitrary Python functions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolCallRequest:
    tool_name: str
    arguments: dict[str, Any]


class ToolExecutor(Protocol):
    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        *,
        allowed_tools: set[str],
    ) -> dict[str, Any]:
        ...


def validate_tool_request(request: ToolCallRequest) -> None:
    """Validate the API-level shape before execution."""
    if not request.tool_name.strip():
        raise ValueError("tool_name is required")

    if not isinstance(request.arguments, dict):
        raise TypeError("arguments must be an object")


def execute_tool_call(
    request: ToolCallRequest,
    executor: ToolExecutor,
    *,
    allowed_tools: set[str],
) -> dict[str, Any]:
    """Validate and execute a single bounded tool request."""
    validate_tool_request(request)

    if request.tool_name not in allowed_tools:
        raise PermissionError("requested tool is not allowed")

    return executor.execute(
        request.tool_name,
        request.arguments,
        allowed_tools=allowed_tools,
    )


def build_tool_call_response(
    request: ToolCallRequest,
    result: dict[str, Any],
) -> dict[str, Any]:
    """Return a stable response envelope for the API layer."""
    return {
        "tool": request.tool_name,
        "status": "completed",
        "result": result,
    }
