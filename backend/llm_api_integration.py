"""
Day 51 — LLM API Integration Patterns

A provider-neutral HTTP client for an LLM-style chat completion endpoint.

The example demonstrates:
- API-key configuration from environment variables
- Explicit request payload construction
- Timeout handling
- Response validation
- Keeping provider-specific details behind a small client boundary
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class LLMConfig:
    base_url: str
    api_key: str
    model: str
    timeout_seconds: float = 15.0


class LLMAPIError(RuntimeError):
    """Raised when an LLM API request cannot be completed safely."""


class LLMClient:
    """Small provider-neutral client for a chat-completion-style API."""

    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    def generate(self, prompt: str) -> str:
        """Send one prompt and return the text content from the response."""
        if not prompt.strip():
            raise ValueError("prompt must not be empty")

        payload = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        request = Request(
            self.config.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                body = json.load(response)
        except (HTTPError, URLError, TimeoutError) as exc:
            raise LLMAPIError("LLM API request failed") from exc
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise LLMAPIError("LLM API returned invalid JSON") from exc

        try:
            content = body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMAPIError("LLM API response has an unexpected shape") from exc

        if not isinstance(content, str):
            raise LLMAPIError("LLM API returned non-text content")

        return content


def load_config() -> LLMConfig:
    """Load configuration without placing credentials in source control."""
    api_key = os.environ.get("LLM_API_KEY")
    base_url = os.environ.get("LLM_API_BASE_URL")
    model = os.environ.get("LLM_MODEL")

    if not api_key or not base_url or not model:
        raise RuntimeError(
            "Set LLM_API_KEY, LLM_API_BASE_URL, and LLM_MODEL before use."
        )

    return LLMConfig(base_url=base_url, api_key=api_key, model=model)
