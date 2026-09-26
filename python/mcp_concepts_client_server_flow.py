"""
Day 57 — Model Context Protocol (MCP) Concepts

Provider-neutral educational example of an MCP-style client/server flow.
The classes model the important boundary without depending on an MCP SDK.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: dict[str, Any]


@dataclass(frozen=True)
class ResourceDefinition:
    uri: str
    name: str
    description: str


class MCPServer(Protocol):
    def list_tools(self) -> list[ToolDefinition]: ...

    def list_resources(self) -> list[ResourceDefinition]: ...

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any: ...

    def read_resource(self, uri: str) -> str: ...


class DemoMCPServer:
    def list_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="add",
                description="Add two integers.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "left": {"type": "integer"},
                        "right": {"type": "integer"},
                    },
                    "required": ["left", "right"],
                },
            )
        ]

    def list_resources(self) -> list[ResourceDefinition]:
        return [
            ResourceDefinition(
                uri="config://application",
                name="Application Configuration",
                description="Read-only application configuration.",
            )
        ]

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        if name != "add":
            raise KeyError(f"unknown tool: {name}")

        return arguments["left"] + arguments["right"]

    def read_resource(self, uri: str) -> str:
        if uri != "config://application":
            raise KeyError(f"unknown resource: {uri}")

        return "environment=demo"


class MCPClient:
    def __init__(self, server: MCPServer) -> None:
        self.server = server

    def discover(self) -> dict[str, list[Any]]:
        return {
            "tools": self.server.list_tools(),
            "resources": self.server.list_resources(),
        }

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        return self.server.call_tool(name, arguments)

    def read_resource(self, uri: str) -> str:
        return self.server.read_resource(uri)


if __name__ == "__main__":
    client = MCPClient(DemoMCPServer())

    print(client.discover())
    print(client.call_tool("add", {"left": 10, "right": 20}))
    print(client.read_resource("config://application"))
