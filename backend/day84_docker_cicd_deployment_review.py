"""Day 84 — Docker, CI/CD, and deployment review helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeploymentConfig:
    """Minimal validated deployment settings for a service."""

    image: str
    replicas: int
    health_path: str
    rollback_image: str | None = None

    def validate(self) -> None:
        if not self.image or ":" not in self.image:
            raise ValueError("image must include an explicit tag or digest")
        if self.replicas < 1:
            raise ValueError("replicas must be at least one")
        if not self.health_path.startswith("/"):
            raise ValueError("health_path must be an absolute path")
        if self.rollback_image == self.image:
            raise ValueError("rollback image must differ from the new image")


def deployment_gate(
    tests_passed: bool,
    image_scan_passed: bool,
    config_valid: bool,
) -> tuple[bool, list[str]]:
    """Return whether deployment can proceed and list failed gates."""
    failures = []
    if not tests_passed:
        failures.append("tests")
    if not image_scan_passed:
        failures.append("image_scan")
    if not config_valid:
        failures.append("configuration")
    return not failures, failures


def run_smoke_tests() -> None:
    config = DeploymentConfig(
        image="registry.example.com/task-api:1.4.0",
        replicas=3,
        health_path="/health/ready",
        rollback_image="registry.example.com/task-api:1.3.2",
    )
    config.validate()
    assert deployment_gate(True, True, True) == (True, [])
    assert deployment_gate(True, False, True) == (False, ["image_scan"])
    try:
        DeploymentConfig("task-api", 0, "health").validate()
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid deployment configuration should fail")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 84 deployment review checks passed.")
