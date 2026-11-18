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


def test_generator_abstains_when_any_citation_is_unknown():
    provider = FakeProvider("Supported [source:handbook], unsupported [source:other].")
    answer = GroundedAnswerGenerator(provider).generate("Question?", [result()])
    assert answer.abstained
    assert answer.source_ids == ()


def test_generator_preserves_provider_failures_for_caller():
    class FailingProvider:
        def complete(self, prompt):
            raise RuntimeError("provider unavailable")

    with pytest.raises(RuntimeError, match="provider unavailable"):
        GroundedAnswerGenerator(FailingProvider()).generate("Question?", [result()])


def test_generator_does_not_call_provider_when_retrieved_context_is_blank():
    provider = FakeProvider("should not be called")
    blank = RetrievalResult(DocumentChunk("blank", "  "), 0.0)
    answer = GroundedAnswerGenerator(provider).generate("Question?", [blank])
    assert answer.abstained
    assert provider.prompt is None


def test_chat_provider_wraps_transport_and_invalid_response_errors(monkeypatch):
    import json
    import urllib.error

    from rag_generation import OpenAIChatCompletionProvider

    provider = OpenAIChatCompletionProvider(api_key="test-key")

    def transport_failure(request, timeout):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr("urllib.request.urlopen", transport_failure)
    with pytest.raises(RuntimeError, match="Answer provider request failed"):
        provider.complete("question")

    def malformed_response(request, timeout):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps({"unexpected": []}).encode()

        return Response()

    monkeypatch.setattr("urllib.request.urlopen", malformed_response)
    with pytest.raises(RuntimeError, match="Answer provider request failed"):
        provider.complete("question")


def test_chat_provider_requires_key_and_positive_timeout(monkeypatch):
    from rag_generation import OpenAIChatCompletionProvider

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        OpenAIChatCompletionProvider(api_key="")
    with pytest.raises(ValueError, match="timeout"):
        OpenAIChatCompletionProvider(api_key="test-key", timeout=0)



def test_chat_provider_sends_configured_model_and_parses_answer(monkeypatch):
    import json

    from rag_generation import OpenAIChatCompletionProvider

    captured = {}

    def successful_response(request, timeout):
        captured["payload"] = json.loads(request.data.decode())
        captured["timeout"] = timeout

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps({
                    "choices": [{"message": {"content": "Grounded answer [source:handbook]."}}]
                }).encode()

        return Response()

    monkeypatch.setattr("urllib.request.urlopen", successful_response)
    provider = OpenAIChatCompletionProvider(api_key="test-key", model="test-model", timeout=5)
    assert provider.complete("question") == "Grounded answer [source:handbook]."
    assert captured["payload"]["model"] == "test-model"
    assert captured["timeout"] == 5
    system_message = captured["payload"]["messages"][0]["content"]
    assert "untrusted data" in system_message
