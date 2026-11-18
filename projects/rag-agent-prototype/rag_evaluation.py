"""Deterministic retrieval evaluation for the RAG prototype."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rag_agent import LexicalRetriever


@dataclass(frozen=True)
class EvaluationCase:
    question: str
    relevant_source_ids: frozenset[str]


@dataclass(frozen=True)
class RetrievalEvaluation:
    case_count: int
    precision_at_k: float
    recall_at_k: float
    mean_reciprocal_rank: float


def load_evaluation_cases(path: str | Path) -> list[EvaluationCase]:
    """Load a small, version-controlled retrieval evaluation set."""
    payload: Any = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("cases"), list):
        raise TypeError("evaluation dataset must contain a cases list")

    cases = []
    for item in payload["cases"]:
        if not isinstance(item, dict):
            raise TypeError("each evaluation case must be an object")
        question = item.get("question")
        source_ids = item.get("relevant_source_ids")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("evaluation questions must be non-empty strings")
        if not isinstance(source_ids, list) or not source_ids or not all(
            isinstance(source_id, str) and source_id.strip() for source_id in source_ids
        ):
            raise ValueError("each case must include relevant source identifiers")
        cases.append(EvaluationCase(question, frozenset(source_ids)))
    return cases


def evaluate_retrieval(
    retriever: LexicalRetriever,
    cases: list[EvaluationCase],
    top_k: int = 3,
) -> RetrievalEvaluation:
    """Calculate macro Precision@K, Recall@K, and MRR over a fixed test set."""
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    if not cases:
        raise ValueError("at least one evaluation case is required")

    precision_total = recall_total = reciprocal_rank_total = 0.0
    for case in cases:
        results = retriever.search(case.question, top_k=top_k)
        retrieved_ids = [result.chunk.document_id for result in results]
        relevant_hits = set(retrieved_ids) & case.relevant_source_ids
        precision_total += len(relevant_hits) / top_k
        recall_total += len(relevant_hits) / len(case.relevant_source_ids)
        first_relevant_rank = next(
            (rank for rank, source_id in enumerate(retrieved_ids, start=1)
             if source_id in case.relevant_source_ids),
            None,
        )
        if first_relevant_rank is not None:
            reciprocal_rank_total += 1 / first_relevant_rank

    count = len(cases)
    return RetrievalEvaluation(
        case_count=count,
        precision_at_k=precision_total / count,
        recall_at_k=recall_total / count,
        mean_reciprocal_rank=reciprocal_rank_total / count,
    )
