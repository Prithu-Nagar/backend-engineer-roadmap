from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_agent import DocumentChunk, RetrievalResult
from rag_generation import GroundedAnswerGenerator


class FakeProvider:
    def __init__(self, answer):
        self.answer = answer
        self.prompt = None

    def complete(self, prompt):
        self.prompt = prompt
        return self.answer


def result(source="handbook", text="RAG uses retrieval to provide context."):
    return RetrievalResult(DocumentChunk(source, text), 0.9)


def test_grounded_answer_returns_valid_source_references():
    provider = FakeProvider("RAG supplies retrieved context [source:handbook].")
    answer = GroundedAnswerGenerator(provider).generate("What does RAG do?", [result()])
    assert not answer.abstained
    assert answer.source_ids == ("handbook",)
    assert "[source:handbook]" in provider.prompt


@pytest.mark.parametrize("response", ["INSUFFICIENT_CONTEXT", ""])
def test_generator_abstains_when_provider_has_no_supported_answer(response):
    answer = GroundedAnswerGenerator(FakeProvider(response)).generate("Question?", [result()])
    assert answer.abstained
    assert not answer.source_ids


def test_generator_rejects_missing_or_unknown_citations():
    for response in ("An uncited claim.", "Claim [source:invented]."):
        answer = GroundedAnswerGenerator(FakeProvider(response)).generate("Question?", [result()])
        assert answer.abstained


def test_generator_abstains_without_retrieval():
    provider = FakeProvider("should not be called")
    answer = GroundedAnswerGenerator(provider).generate("Question?", [])
    assert answer.abstained
    assert provider.prompt is None


def test_generator_validates_question_and_limits():
    with pytest.raises(ValueError):
        GroundedAnswerGenerator(FakeProvider("x")).generate(" ", [result()])
    with pytest.raises(ValueError):
        GroundedAnswerGenerator(FakeProvider("x"), max_sources=0)


def test_generator_bounds_number_of_sources_and_context():
    provider = FakeProvider("Supported [source:first].")
    generator = GroundedAnswerGenerator(provider, max_context_chars=100, max_sources=1)
    generator.generate("Question?", [result("first"), result("second")])
    assert "[source:first]" in provider.prompt
    assert "[source:second]" not in provider.prompt
    assert len(provider.prompt) < 500
