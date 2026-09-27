"""
Day 58 — AI Service Testing

Provider-neutral testing boundary for an AI service with deterministic
dependency doubles and explicit failure handling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AIRequest:
    prompt: str


@dataclass(frozen=True)
class AIResponse:
    text: str
    model: str


class AIProvider(Protocol):
    def generate(self, prompt: str) -> AIResponse: ...


class FakeAIProvider:
    def __init__(
        self,
        response: AIResponse | None = None,
        error: Exception | None = None,
    ) -> None:
        self.response = response or AIResponse("fake answer", "fake-model")
        self.error = error
        self.calls: list[str] = []

    def generate(self, prompt: str) -> AIResponse:
        self.calls.append(prompt)
        if self.error is not None:
            raise self.error
        return self.response


class AIService:
    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider

    def generate(self, request: AIRequest) -> AIResponse:
        if not request.prompt.strip():
            raise ValueError("prompt must not be empty")

        response = self.provider.generate(request.prompt)

        if not response.text.strip():
            raise ValueError("provider returned empty output")

        return AIResponse(response.text.strip(), response.model)


def test_successful_generation() -> None:
    provider = FakeAIProvider(AIResponse("  answer  ", "test-model"))
    service = AIService(provider)

    response = service.generate(AIRequest("question"))

    assert response == AIResponse("answer", "test-model")
    assert provider.calls == ["question"]


def test_invalid_input() -> None:
    service = AIService(FakeAIProvider())

    try:
        service.generate(AIRequest(" "))
    except ValueError as exc:
        assert str(exc) == "prompt must not be empty"
    else:
        raise AssertionError("Expected ValueError")


def test_provider_failure_is_visible() -> None:
    provider = FakeAIProvider(error=TimeoutError("provider timeout"))
    service = AIService(provider)

    try:
        service.generate(AIRequest("question"))
    except TimeoutError as exc:
        assert str(exc) == "provider timeout"
    else:
        raise AssertionError("Expected TimeoutError")


if __name__ == "__main__":
    test_successful_generation()
    test_invalid_input()
    test_provider_failure_is_visible()
    print("AI service tests passed.")
