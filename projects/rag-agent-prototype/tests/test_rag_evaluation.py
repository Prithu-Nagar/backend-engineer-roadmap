from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from rag_agent import DocumentChunk, LexicalRetriever
from rag_evaluation import EvaluationCase, evaluate_retrieval, load_evaluation_cases


def test_fixed_evaluation_dataset_measures_retrieval_quality():
    cases = load_evaluation_cases(PROJECT_ROOT / "evaluation_cases.json")
    retriever = LexicalRetriever([
        DocumentChunk("backend-rate-limits", "AI endpoints use tenant-aware rate limits and token budgets to control cost."),
        DocumentChunk("rag-retrieval", "RAG separates document ingestion, chunking, retrieval, context assembly, and answer generation."),
        DocumentChunk("ai-reliability", "AI services use bounded retries, timeouts, fallbacks, and stable client-facing errors."),
    ])

    metrics = evaluate_retrieval(retriever, cases, top_k=2)

    assert metrics.case_count == 3
    assert metrics.precision_at_k == pytest.approx(0.5)
    assert metrics.recall_at_k == pytest.approx(1.0)
    assert metrics.mean_reciprocal_rank == pytest.approx(1.0)


def test_evaluation_rejects_invalid_dataset_and_parameters(tmp_path):
    invalid = tmp_path / "invalid.json"
    invalid.write_text('{"cases":[{"question":" " ,"relevant_source_ids":["doc"]}]}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_evaluation_cases(invalid)
    with pytest.raises(ValueError):
        evaluate_retrieval(LexicalRetriever([]), [], top_k=1)
    with pytest.raises(ValueError):
        evaluate_retrieval(LexicalRetriever([]), [EvaluationCase("question", frozenset({"doc"}))], top_k=0)
