"""
Day 49 — Production Debugging

A small, dependency-free incident-debugging toolkit for Python services.
The workflow separates symptom collection, hypothesis tracking, and evidence
collection so production debugging does not become guesswork.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
import time
import traceback
from typing import Callable, TypeVar


logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class DebugContext:
    """Evidence collected while investigating a production failure."""

    incident_id: str
    symptoms: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    def add_symptom(self, symptom: str) -> None:
        self.symptoms.append(symptom)

    def add_hypothesis(self, hypothesis: str) -> None:
        self.hypotheses.append(hypothesis)

    def record_evidence(self, evidence: str) -> None:
        self.evidence.append(evidence)


def measure_call(
    operation: Callable[..., T],
    *args: object,
    **kwargs: object,
) -> tuple[T, float]:
    """Run an operation and return its result with elapsed time."""

    started = time.perf_counter()
    try:
        return operation(*args, **kwargs), time.perf_counter() - started
    except Exception:
        logger.exception("production_operation_failed")
        raise


def safe_exception_summary(error: BaseException) -> str:
    """Return a diagnostic summary without exposing request secrets."""

    return f"{type(error).__name__}: {error}"


def capture_traceback(error: BaseException) -> str:
    """Capture a traceback for internal diagnostics."""

    return "".join(traceback.format_exception(type(error), error, error.__traceback__))


if __name__ == "__main__":
    context = DebugContext("INC-049")
    context.add_symptom("Elevated 5xx responses")
    context.add_hypothesis("A downstream dependency is timing out")
    context.record_evidence("Readiness check reports the dependency as unavailable")
    print(context)
