"""Document ingestion, chunking, embeddings, and in-memory vector retrieval.

The OpenAI adapter performs real remote embedding requests. The hashing
adapter is an explicitly local, deterministic fallback for tests and demos; it
is not a semantic embedding model.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import urllib.error
import urllib.request
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from rag_agent import DocumentChunk, RetrievalResult


@dataclass(frozen=True)
class SourceDocument:
    document_id: str
    text: str
    metadata: Mapping[str, str] = field(default_factory=dict)


def load_text_file(
    path: str | Path,
    document_id: str | None = None,
    metadata: Mapping[str, str] | None = None,
) -> SourceDocument:
    """Load a UTF-8 text or Markdown file as a source document."""
    file_path = Path(path)
    source_metadata = dict(metadata or {})
    source_metadata.setdefault("source", str(file_path))
    return SourceDocument(
        document_id=document_id or file_path.stem,
        text=file_path.read_text(encoding="utf-8"),
        metadata=source_metadata,
    )


class EmbeddingProvider(Protocol):
    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


class OpenAIEmbeddingProvider:
    """Small OpenAI embeddings adapter using the standard library HTTP client."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "text-embedding-3-small",
        timeout: float = 20.0,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for live embeddings")
        self.model = model
        self.timeout = timeout

    def _embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        payload = json.dumps({"model": self.model, "input": list(texts)}).encode()
        request = urllib.request.Request(
            "https://api.openai.com/v1/embeddings",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError("Embedding provider request failed") from exc
        try:
            items = sorted(body["data"], key=lambda item: item["index"])
            vectors = [[float(value) for value in item["embedding"]] for item in items]
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError("Embedding provider returned an invalid response") from exc
        if len(vectors) != len(texts) or any(not vector for vector in vectors):
            raise RuntimeError("Embedding provider returned an unexpected vector count")
        dimensions = len(vectors[0])
        if any(len(vector) != dimensions for vector in vectors):
            raise RuntimeError("Embedding provider returned inconsistent dimensions")
        return vectors

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return self._embed(texts)

    def embed_query(self, text: str) -> list[float]:
        vectors = self._embed([text])
        return vectors[0]


class HashingEmbeddingProvider:
    """Deterministic local feature hashing; useful for tests, not semantic search."""

    def __init__(self, dimensions: int = 256) -> None:
        if dimensions < 8:
            raise ValueError("dimensions must be at least 8")
        self.dimensions = dimensions

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[index] += 1.0 if digest[4] % 2 else -1.0
        magnitude = math.sqrt(sum(value * value for value in vector))
        return [value / magnitude for value in vector] if magnitude else vector

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


class DocumentChunker:
    """Split source text into bounded, overlapping chunks with stable metadata."""

    def __init__(self, chunk_size: int = 800, overlap: int = 120) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("overlap must be non-negative and smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, document: SourceDocument) -> list[DocumentChunk]:
        text = document.text.strip()
        if not text:
            return []
        chunks: list[DocumentChunk] = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            if end < len(text):
                boundary = text.rfind(" ", start, end)
                if boundary > start:
                    end = boundary
            chunk_text = text[start:end].strip()
            if chunk_text:
                metadata = dict(document.metadata)
                metadata.update({"chunk_index": str(len(chunks)), "start_char": str(start), "end_char": str(end)})
                chunks.append(DocumentChunk(document.document_id, chunk_text, metadata))
            if end >= len(text):
                break
            start = max(end - self.overlap, start + 1)
        return chunks


@dataclass(frozen=True)
class VectorRecord:
    chunk: DocumentChunk
    embedding: tuple[float, ...]


class InMemoryVectorStore:
    """Simple in-process cosine-similarity store; data is not persisted."""

    def __init__(self) -> None:
        self._records: list[VectorRecord] = []
        self._dimensions: int | None = None

    def add(self, chunks: Sequence[DocumentChunk], embeddings: Sequence[Sequence[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Each chunk must have exactly one embedding")
        for chunk, embedding in zip(chunks, embeddings):
            vector = tuple(float(value) for value in embedding)
            if not vector:
                raise ValueError("Embeddings cannot be empty")
            if self._dimensions is None:
                self._dimensions = len(vector)
            if len(vector) != self._dimensions:
                raise ValueError("Embedding dimensions do not match the vector store")
            self._records.append(VectorRecord(chunk, vector))

    @staticmethod
    def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))
        if not left_norm or not right_norm:
            return 0.0
        return sum(a * b for a, b in zip(left, right)) / (left_norm * right_norm)

    def search(self, query_embedding: Sequence[float], top_k: int = 3) -> list[RetrievalResult]:
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        query = tuple(float(value) for value in query_embedding)
        if self._dimensions is not None and len(query) != self._dimensions:
            raise ValueError("Query embedding dimensions do not match the vector store")
        results = [
            RetrievalResult(record.chunk, self._cosine(query, record.embedding))
            for record in self._records
        ]
        results.sort(key=lambda result: (-result.score, result.chunk.document_id,
                                          result.chunk.metadata.get("chunk_index", "")))
        return results[:top_k]

    def __len__(self) -> int:
        return len(self._records)


class DocumentIngestionPipeline:
    def __init__(self, chunker: DocumentChunker, embedder: EmbeddingProvider, store: InMemoryVectorStore) -> None:
        self.chunker = chunker
        self.embedder = embedder
        self.store = store

    def ingest(self, documents: Sequence[SourceDocument]) -> list[DocumentChunk]:
        chunks = [chunk for document in documents for chunk in self.chunker.split(document)]
        if chunks:
            embeddings = self.embedder.embed_documents([chunk.text for chunk in chunks])
            self.store.add(chunks, embeddings)
        return chunks


class VectorRetriever:
    def __init__(self, embedder: EmbeddingProvider, store: InMemoryVectorStore) -> None:
        self.embedder = embedder
        self.store = store

    def search(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        if not query.strip():
            return []
        return self.store.search(self.embedder.embed_query(query), top_k=top_k)
