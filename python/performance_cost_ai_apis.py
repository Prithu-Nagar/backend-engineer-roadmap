"""
Day 59 — Performance and Cost Considerations for AI APIs

Provider-neutral patterns for measuring latency, estimating token cost,
and choosing bounded execution strategies for AI API calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Callable, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class ModelPricing:
    input_cost_per_million: float
    output_cost_per_million: float


@dataclass(frozen=True)
class Usage:
    input_tokens: int
    output_tokens: int
    latency_ms: float


def estimate_cost(usage: Usage, pricing: ModelPricing) -> float:
    """Estimate request cost from token usage and model pricing."""
    return (
        usage.input_tokens * pricing.input_cost_per_million / 1_000_000
        + usage.output_tokens * pricing.output_cost_per_million / 1_000_000
    )


def measure_latency(operation: Callable[[], T]) -> tuple[T, float]:
    """Run an operation and return its result with measured latency."""
    started = perf_counter()
    result = operation()
    elapsed_ms = (perf_counter() - started) * 1000
    return result, elapsed_ms


def choose_execution_mode(
    *,
    estimated_input_tokens: int,
    requires_low_latency: bool,
    cache_hit: bool,
) -> str:
    """Select a simple execution policy before calling an AI provider."""
    if cache_hit:
        return "cache"

    if requires_low_latency and estimated_input_tokens <= 1_000:
        return "fast-model"

    if estimated_input_tokens > 8_000:
        return "context-reduction-or-batch"

    return "standard-model"


if __name__ == "__main__":
    usage = Usage(input_tokens=2_000, output_tokens=500, latency_ms=420)
    pricing = ModelPricing(
        input_cost_per_million=2.00,
        output_cost_per_million=8.00,
    )

    print(f"Estimated cost: ${estimate_cost(usage, pricing):.6f}")
    print(
        choose_execution_mode(
            estimated_input_tokens=usage.input_tokens,
            requires_low_latency=True,
            cache_hit=False,
        )
    )
