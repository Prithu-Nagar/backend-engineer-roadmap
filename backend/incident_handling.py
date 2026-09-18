"""
Day 49 — Incident Handling

Defines a small incident lifecycle for backend services:
detect -> assess -> mitigate -> recover -> review.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class IncidentSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentState(StrEnum):
    DETECTED = "detected"
    ASSESSING = "assessing"
    MITIGATING = "mitigating"
    RECOVERING = "recovering"
    RESOLVED = "resolved"


@dataclass
class Incident:
    incident_id: str
    severity: IncidentSeverity
    summary: str
    state: IncidentState = IncidentState.DETECTED
    actions: list[str] = field(default_factory=list)

    def transition(self, state: IncidentState, action: str) -> None:
        """Record a state transition and the operational action taken."""

        self.state = state
        self.actions.append(action)

    def resolve(self, action: str = "Service health verified") -> None:
        """Mark the incident resolved after recovery validation."""

        self.transition(IncidentState.RESOLVED, action)


def build_incident_runbook(incident: Incident) -> list[str]:
    """Return the ordered response checklist for an incident."""

    return [
        f"Confirm impact for {incident.incident_id}: {incident.summary}",
        "Assign incident owner and establish an incident timeline",
        "Collect logs, metrics, traces, and database evidence",
        "Stop or isolate the failing change when necessary",
        "Choose mitigation: rollback, traffic reduction, dependency isolation, or recovery mode",
        "Verify service health and error-rate recovery",
        "Record root cause, contributing factors, and follow-up actions",
    ]


if __name__ == "__main__":
    incident = Incident(
        incident_id="INC-049",
        severity=IncidentSeverity.HIGH,
        summary="Elevated API error rate after deployment",
    )
    incident.transition(IncidentState.ASSESSING, "Compared error rate with deployment timeline")
    incident.transition(IncidentState.MITIGATING, "Prepared rollback")
    incident.transition(IncidentState.RECOVERING, "Rolled back and monitored health checks")
    incident.resolve()
    for step in build_incident_runbook(incident):
        print(step)
