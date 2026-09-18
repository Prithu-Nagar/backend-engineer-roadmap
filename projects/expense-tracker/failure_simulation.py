"""
Day 49 — Expense Tracker Failure Simulation

Simulates a controlled dependency failure and records the operational
decisions that would be used during a real incident.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class RecoveryMode(StrEnum):
    NORMAL = "normal"
    DEGRADED = "degraded"
    RECOVERING = "recovering"


@dataclass
class FailureSimulation:
    dependency: str
    recovery_mode: RecoveryMode = RecoveryMode.NORMAL
    events: list[str] = field(default_factory=list)
    rollback_required: bool = False

    def fail_dependency(self, reason: str) -> None:
        self.events.append(f"dependency_failed:{self.dependency}:{reason}")
        self.recovery_mode = RecoveryMode.DEGRADED

    def enter_recovery(self, reason: str) -> None:
        self.events.append(f"recovery_started:{reason}")
        self.recovery_mode = RecoveryMode.RECOVERING

    def restore(self) -> None:
        self.events.append("dependency_restored")
        self.recovery_mode = RecoveryMode.NORMAL

    def request_rollback(self, release: str) -> None:
        self.rollback_required = True
        self.events.append(f"rollback_requested:{release}")


def run_failure_simulation() -> FailureSimulation:
    """Run a deterministic failure/recovery scenario."""

    simulation = FailureSimulation("postgresql")
    simulation.fail_dependency("connection timeout")
    simulation.request_rollback("release-49")
    simulation.enter_recovery("serve safe reads and stop new aggregation work")
    simulation.restore()
    return simulation


if __name__ == "__main__":
    print(run_failure_simulation())
