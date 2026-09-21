"""
Day 52 — Embeddings + Vector Retrieval Pipeline

A dependency-free example of the application boundary between embedding
creation and vector retrieval. The embedding provider and vector database are
represented by small interfaces so they can be replaced independently.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence


@dataclass(frozen=True)
class Chunk:
    id: int
    document_id: int
    tenant_id: int
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: Chunk
    score: float


class Embedder(Protocol):
    def embed(self, text: str) -> Sequence[float]: ...


class VectorStore(Protocol):
    def upsert(self, chunk: Chunk, vector: Sequence[float]) -> None: ...

    def search(
        self,
        vector: Sequence[float],
        tenant_id: int,
        limit: int,
    ) -> list[RetrievedChunk]: ...


class RetrievalPipeline:
    """Coordinates embedding generation and tenant-scoped retrieval."""

    def __init__(self, embedder: Embedder, store: VectorStore) -> None:
        self.embedder = embedder
        self.store = store

    def index_chunk(self, chunk: Chunk) -> None:
        vector = self.embedder.embed(chunk.text)
        if not vector:
            raise ValueError("embedding must not be empty")
        self.store.upsert(chunk, vector)

    def retrieve(self, query: str, tenant_id: int, limit: int = 5) -> list[RetrievedChunk]:
        if not query.strip():
            raise ValueError("query must not be empty")
        if limit <= 0:
            raise ValueError("limit must be positive")

        query_vector = self.embedder.embed(query)
        if not query_vector:
            raise ValueError("query embedding must not be empty")

        return self.store.search(query_vector, tenant_id=tenant_id, limit=limit)
