"""
Day 57 — MCP-Enabled Backend Concept

Provider-neutral backend boundary for exposing approved tools and resources
through an MCP-style adapter while keeping application services separate from
the protocol layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolRequest:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ResourceRequest:
    uri: str


class ApplicationTool(Protocol):
    name: str

    def execute(self, arguments: dict[str, Any]) -> dict[str, Any]: ...


class ApplicationResource(Protocol):
    uri: str

    def read(self) -> str: ...


class AddTool:
    name = "add"

    def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        left = arguments.get("left")
        right = arguments.get("right")

        if not isinstance(left, int) or not isinstance(right, int):
            raise ValueError("left and right must be integers")

        return {"value": left + right}


class ApplicationConfigResource:
    uri = "config://application"

    def read(self) -> str:
        return "environment=demo"


class MCPAdapter:
    def __init__(
        self,
        tools: list[ApplicationTool],
        resources: list[ApplicationResource],
    ) -> None:
        self._tools = {tool.name: tool for tool in tools}
        self._resources = {resource.uri: resource for resource in resources}

    def call_tool(self, request: ToolRequest) -> dict[str, Any]:
        tool = self._tools.get(request.name)
        if tool is None:
            raise KeyError(f"tool not exposed: {request.name}")

        return tool.execute(request.arguments)

    def read_resource(self, request: ResourceRequest) -> str:
        resource = self._resources.get(request.uri)
        if resource is None:
            raise KeyError(f"resource not exposed: {request.uri}")

        return resource.read()


if __name__ == "__main__":
    adapter = MCPAdapter(
        tools=[AddTool()],
        resources=[ApplicationConfigResource()],
    )

    print(adapter.call_tool(ToolRequest("add", {"left": 4, "right": 6})))
    print(adapter.read_resource(ResourceRequest("config://application")))
