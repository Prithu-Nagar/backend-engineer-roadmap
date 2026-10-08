"""Pagination and caching patterns for a read-heavy backend.

The example keeps cache policy explicit and uses cursor pagination so deep
pages do not require increasingly expensive OFFSET scans.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Protocol


@dataclass(frozen=True)
class FeedItem:
    post_id: int
    author_id: int
    created_at: float


@dataclass(frozen=True)
class Page:
    items: list[FeedItem]
    next_cursor: int | None


class FeedRepository(Protocol):
    def fetch_page(self, viewer_id: int, before_id: int | None, limit: int) -> Page:
        """Fetch a stable cursor-based page from durable storage."""


class Cache(Protocol):
    def get(self, key: str) -> Page | None:
        """Return a cached page or None on a miss."""

    def set(self, key: str, value: Page, ttl_seconds: float) -> None:
        """Store a bounded-lifetime page."""

    def delete(self, key: str) -> None:
        """Invalidate one cached page."""


class FeedService:
    """Serve feed pages while keeping cache behavior observable and bounded."""

    def __init__(
        self,
        repository: FeedRepository,
        cache: Cache,
        ttl_seconds: float = 30.0,
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.repository = repository
        self.cache = cache
        self.ttl_seconds = ttl_seconds

    @staticmethod
    def cache_key(viewer_id: int, before_id: int | None, limit: int) -> str:
        cursor = "first" if before_id is None else str(before_id)
        return f"feed:{viewer_id}:{cursor}:{limit}"

    def get_page(
        self,
        *,
        viewer_id: int,
        before_id: int | None,
        limit: int = 50,
    ) -> Page:
        if viewer_id <= 0:
            raise ValueError("viewer_id must be positive")
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")

        key = self.cache_key(viewer_id, before_id, limit)
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        page = self.repository.fetch_page(viewer_id, before_id, limit)
        self.cache.set(key, page, self.ttl_seconds)
        return page

    def invalidate_first_page(self, viewer_id: int) -> None:
        """Invalidate the most visible page after a feed-changing event."""
        self.cache.delete(self.cache_key(viewer_id, None, 50))


def record_request_latency(started: float) -> float:
    """Return elapsed milliseconds for simple request-level instrumentation."""
    return (monotonic() - started) * 1000


if __name__ == "__main__":
    print(FeedService.cache_key(42, None, 50))
