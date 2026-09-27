"""
Day 58 — Testing LLM Integrations

Provider-neutral testing patterns for LLM-backed Python services.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    usage_tokens: int


class LLMClient(Protocol):
    def complete(self, prompt: str) -> LLMResponse: ...


class FakeLLMClient:
    """Deterministic test double for an external LLM provider."""

    def __init__(self, response: LLMResponse | None = None) -> None:
        self.calls: list[str] = []
        self.response = response or LLMResponse(
            text="test response",
            model="fake-model",
            usage_tokens=12,
        )

    def complete(self, prompt: str) -> LLMResponse:
        self.calls.append(prompt)
        return self.response


class LLMService:
    def __init__(self, client: LLMClient) -> None:
        self.client = client

    def answer(self, question: str) -> str:
        if not question.strip():
            raise ValueError("question must not be empty")

        response = self.client.complete(question)

        if not response.text.strip():
            raise ValueError("LLM returned an empty response")

        return response.text.strip()


def test_service_uses_client_boundary() -> None:
    client = FakeLLMClient(LLMResponse("hello", "fake-model", 5))
    service = LLMService(client)

    assert service.answer("Say hello") == "hello"
    assert client.calls == ["Say hello"]


def test_service_rejects_empty_question() -> None:
    service = LLMService(FakeLLMClient())

    try:
        service.answer("   ")
    except ValueError as exc:
        assert str(exc) == "question must not be empty"
    else:
        raise AssertionError("Expected ValueError")


def test_service_rejects_empty_model_output() -> None:
    client = FakeLLMClient(LLMResponse("   ", "fake-model", 3))
    service = LLMService(client)

    try:
        service.answer("Generate a response")
    except ValueError as exc:
        assert str(exc) == "LLM returned an empty response"
    else:
        raise AssertionError("Expected ValueError")


if __name__ == "__main__":
    test_service_uses_client_boundary()
    test_service_rejects_empty_question()
    test_service_rejects_empty_model_output()
    print("LLM integration tests passed.")
