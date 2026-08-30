"""
Day 30 — Flask vs Django vs FastAPI

A compact decision aid for selecting a Python backend framework based on
application requirements. This is a learning artifact, not a benchmark.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class BackendRequirements:
    """Requirements that influence framework selection."""

    needs_full_stack_features: bool = False
    needs_django_admin: bool = False
    async_io_heavy: bool = False
    typed_api_contracts: bool = False
    small_service: bool = False


def recommend_framework(requirements: BackendRequirements) -> str:
    """Return a simple recommendation from the supplied requirements."""

    if requirements.needs_django_admin or requirements.needs_full_stack_features:
        return "Django / DRF"

    if requirements.async_io_heavy or requirements.typed_api_contracts:
        return "FastAPI"

    if requirements.small_service:
        return "Flask"

    # When requirements are not decisive, prefer the smallest suitable stack.
    return "Flask"


def framework_strengths() -> dict[str, list[str]]:
    """Return the primary strengths reviewed on Day 30."""

    return {
        "Flask": [
            "Lightweight core",
            "Flexible application structure",
            "Good fit for small focused services",
        ],
        "Django / DRF": [
            "Full-stack framework",
            "Django ORM and admin",
            "Mature authentication and application conventions",
        ],
        "FastAPI": [
            "Typed request and response models",
            "Automatic OpenAPI documentation",
            "Strong async API support",
        ],
    }


if __name__ == "__main__":
    examples = [
        BackendRequirements(small_service=True),
        BackendRequirements(
            needs_full_stack_features=True,
            needs_django_admin=True,
        ),
        BackendRequirements(
            async_io_heavy=True,
            typed_api_contracts=True,
        ),
    ]

    for requirements in examples:
        print(f"{requirements} -> {recommend_framework(requirements)}")
