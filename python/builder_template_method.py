"""
Day 64 — Builder and Template Method Design Patterns in Python

A backend-oriented example showing fluent construction of a request object
through Builder and a fixed workflow with overridable steps through Template
Method.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ApiRequest:
    method: str
    path: str
    headers: dict[str, str]
    body: dict[str, object] | None


class ApiRequestBuilder:
    """Builds an immutable API request through explicit configuration steps."""

    def __init__(self) -> None:
        self._method = "GET"
        self._path = "/"
        self._headers: dict[str, str] = {}
        self._body: dict[str, object] | None = None

    def method(self, method: str) -> ApiRequestBuilder:
        self._method = method.upper()
        return self

    def path(self, path: str) -> ApiRequestBuilder:
        self._path = path
        return self

    def header(self, name: str, value: str) -> ApiRequestBuilder:
        self._headers[name] = value
        return self

    def body(self, body: dict[str, object]) -> ApiRequestBuilder:
        self._body = body
        return self

    def build(self) -> ApiRequest:
        if not self._path.startswith("/"):
            raise ValueError("path must start with '/'")
        if not self._method:
            raise ValueError("method must not be empty")

        return ApiRequest(
            method=self._method,
            path=self._path,
            headers=dict(self._headers),
            body=dict(self._body) if self._body is not None else None,
        )


class RequestProcessor(ABC):
    """Template Method: fixes the workflow while subclasses customize steps."""

    def process(self, request: ApiRequest) -> str:
        self.validate(request)
        normalized = self.normalize(request)
        return self.execute(normalized)

    def validate(self, request: ApiRequest) -> None:
        if not request.path.startswith("/"):
            raise ValueError("invalid request path")

    def normalize(self, request: ApiRequest) -> ApiRequest:
        return request

    @abstractmethod
    def execute(self, request: ApiRequest) -> str:
        """Perform the application-specific operation."""


class LoggingRequestProcessor(RequestProcessor):
    def execute(self, request: ApiRequest) -> str:
        return f"{request.method} {request.path}"


def main() -> None:
    request = (
        ApiRequestBuilder()
        .method("post")
        .path("/api/tasks")
        .header("Content-Type", "application/json")
        .body({"title": "Review design patterns"})
        .build()
    )

    processor = LoggingRequestProcessor()
    print(processor.process(request))


if __name__ == "__main__":
    main()
