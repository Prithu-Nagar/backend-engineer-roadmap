"""
Day 53 — RAG Retrieval Pipeline

Dependency-free reference implementation of chunking, candidate retrieval,
reranking, and bounded context construction.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Chunk:
    chunk_id: int
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class Candidate:
    chunk: Chunk
    retrieval_score: float


def chunk_text(text: str, max_words: int = 80, overlap: int = 10) -> list[str]:
    """Split text into bounded, overlapping word chunks."""
    if max_words <= 0 or overlap < 0 or overlap >= max_words:
        raise ValueError("invalid chunk configuration")

    words = text.split()
    chunks: list[str] = []
    step = max_words - overlap

    for start in range(0, len(words), step):
        chunk = " ".join(words[start : start + max_words])
        if chunk:
            chunks.append(chunk)
        if start + max_words >= len(words):
            break

    return chunks


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def lexical_retrieval(query: str, chunks: list[Chunk], limit: int = 10) -> list[Candidate]:
    """Produce a simple lexical candidate set for demonstration purposes."""
    query_terms = tokenize(query)
    scored = []

    for chunk in chunks:
        terms = tokenize(chunk.text)
        score = len(query_terms & terms) / max(len(query_terms), 1)
        if score > 0:
            scored.append(Candidate(chunk=chunk, retrieval_score=score))

    return sorted(scored, key=lambda item: item.retrieval_score, reverse=True)[:limit]


def rerank(query: str, candidates: list[Candidate], limit: int = 5) -> list[Candidate]:
    """Apply a second relevance signal to a small candidate set."""
    query_terms = tokenize(query)

    def score(candidate: Candidate) -> float:
        terms = tokenize(candidate.chunk.text)
        exact_phrase_bonus = 0.2 if query.lower() in candidate.chunk.text.lower() else 0.0
        overlap = len(query_terms & terms) / max(len(query_terms), 1)
        return candidate.retrieval_score + overlap + exact_phrase_bonus

    return sorted(candidates, key=score, reverse=True)[:limit]


def build_context(candidates: list[Candidate], max_chars: int = 4000) -> str:
    """Construct bounded model context while retaining source boundaries."""
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")

    sections: list[str] = []
    used = 0

    for candidate in candidates:
        section = (
            f"[source:{candidate.chunk.chunk_id} "
            f"score:{candidate.retrieval_score:.3f}]\n"
            f"{candidate.chunk.text}"
        )
        extra = len(section) + (2 if sections else 0)
        if used + extra > max_chars:
            break
        sections.append(section)
        used += extra

    return "\n\n".join(sections)
