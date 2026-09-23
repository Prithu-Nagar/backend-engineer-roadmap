"""
Day 54 — RAG Ingestion Service

A provider-neutral ingestion service that separates document loading,
chunking, embedding, persistence, and asynchronous job execution from the
online RAG query path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SourceDocument:
    document_id: str
    tenant_id: int
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class DocumentChunk:
    document_id: str
    chunk_id: int
    text: str
    metadata: dict[str, str]


class Chunker(Protocol):
    def split(self, document: SourceDocument) -> list[DocumentChunk]: ...


class Embedder(Protocol):
    async def embed(self, chunks: list[DocumentChunk]) -> list[list[float]]: ...


class ChunkRepository(Protocol):
    async def save(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None: ...


class SimpleChunker:
    """Create deterministic word-bounded chunks for demonstration."""

    def __init__(self, words_per_chunk: int = 80) -> None:
        if words_per_chunk <= 0:
            raise ValueError("words_per_chunk must be positive")
        self.words_per_chunk = words_per_chunk

    def split(self, document: SourceDocument) -> list[DocumentChunk]:
        words = document.text.split()
        chunks: list[DocumentChunk] = []

        for index in range(0, len(words), self.words_per_chunk):
            text = " ".join(words[index : index + self.words_per_chunk])
            if text:
                chunks.append(
                    DocumentChunk(
                        document_id=document.document_id,
                        chunk_id=len(chunks) + 1,
                        text=text,
                        metadata=document.metadata,
                    )
                )

        return chunks


class DemoEmbedder:
    async def embed(self, chunks: list[DocumentChunk]) -> list[list[float]]:
        # Replace this deterministic placeholder with a real embedding provider.
        return [[float(len(chunk.text)), float(chunk.chunk_id)] for chunk in chunks]


class InMemoryChunkRepository:
    def __init__(self) -> None:
        self.records: list[tuple[DocumentChunk, list[float]]] = []

    async def save(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        self.records.extend(zip(chunks, embeddings))


class RagIngestionService:
    """Run the offline ingestion pipeline independently of online serving."""

    def __init__(
        self,
        chunker: Chunker,
        embedder: Embedder,
        repository: ChunkRepository,
    ) -> None:
        self.chunker = chunker
        self.embedder = embedder
        self.repository = repository

    async def ingest(self, document: SourceDocument) -> int:
        chunks = self.chunker.split(document)
        if not chunks:
            return 0

        embeddings = await self.embedder.embed(chunks)
        if len(embeddings) != len(chunks):
            raise ValueError("embedding count must match chunk count")

        await self.repository.save(chunks, embeddings)
        return len(chunks)
