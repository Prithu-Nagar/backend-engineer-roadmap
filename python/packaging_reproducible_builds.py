"""
Day 44 — Packaging and Reproducible Builds

This module demonstrates the repository metadata and dependency practices that
make a Python application easier to build consistently across environments.
"""

from __future__ import annotations


BUILD_PRACTICES = {
    "project_metadata": "pyproject.toml",
    "dependency_constraints": "requirements.txt or a lock file",
    "isolated_environment": "python -m venv .venv",
    "build_artifact": "python -m build",
    "verification": "Install the built artifact in a clean environment and run tests.",
}


def reproducibility_checklist() -> list[str]:
    """Return practical checks for a reproducible Python build."""

    return [
        "Pin or constrain dependency versions.",
        "Keep project metadata and build configuration under version control.",
        "Build from a clean, isolated environment.",
        "Produce the same artifact from the same source revision.",
        "Install the artifact in a clean environment before release.",
        "Run automated tests against the built artifact.",
    ]


def build_artifact_flow() -> tuple[str, ...]:
    """Describe the normal source-to-artifact workflow."""

    return (
        "Source revision",
        "Install declared build dependencies",
        "Build wheel and source distribution",
        "Verify artifact metadata",
        "Install artifact in clean environment",
        "Run tests",
    )


if __name__ == "__main__":
    print(BUILD_PRACTICES)
    print(reproducibility_checklist())
    print(build_artifact_flow())
