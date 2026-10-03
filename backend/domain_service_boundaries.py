"""
Day 64 — Domain / Service Boundaries

A framework-neutral URL Shortener example showing a small domain model,
application service, and repository contract. The service owns use-case policy
while persistence remains behind an explicit boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urlparse


@dataclass(frozen=True)
class ShortURL:
    short_code: str
    original_url: str


class ShortURLRepository(Protocol):
    def get_by_code(self, short_code: str) -> ShortURL | None:
        ...

    def save(self, short_url: ShortURL) -> ShortURL:
        ...


class InMemoryShortURLRepository:
    def __init__(self) -> None:
        self._items: dict[str, ShortURL] = {}

    def get_by_code(self, short_code: str) -> ShortURL | None:
        return self._items.get(short_code)

    def save(self, short_url: ShortURL) -> ShortURL:
        self._items[short_url.short_code] = short_url
        return short_url


class URLShortenerService:
    """Application service containing the create-short-url use case."""

    def __init__(self, repository: ShortURLRepository) -> None:
        self._repository = repository

    def create_short_url(
        self,
        *,
        short_code: str,
        original_url: str,
    ) -> ShortURL:
        if not short_code.strip():
            raise ValueError("short_code must not be empty")

        parsed = urlparse(original_url.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("original_url must be a valid HTTP(S) URL")

        normalized_code = short_code.strip()
        if self._repository.get_by_code(normalized_code) is not None:
            raise ValueError("short_code already exists")

        return self._repository.save(
            ShortURL(normalized_code, original_url.strip())
        )


def build_application() -> URLShortenerService:
    return URLShortenerService(InMemoryShortURLRepository())


if __name__ == "__main__":
    service = build_application()
    print(
        service.create_short_url(
            short_code="aB91x",
            original_url="https://example.com/backend",
        )
    )
