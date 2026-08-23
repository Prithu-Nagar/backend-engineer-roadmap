"""
Day 23 — Python Packaging, Virtual Environments & Dependencies

This file demonstrates the practical workflow used to isolate a Python
backend project, declare dependencies, and make the environment reproducible.
The commands are shown as examples and are not executed by this module.
"""

from __future__ import annotations


PROJECT_SETUP = {
    "create_environment": "python -m venv .venv",
    "activate_windows": ".venv\\Scripts\\activate",
    "activate_unix": "source .venv/bin/activate",
    "install_dependency": "python -m pip install django djangorestframework",
    "freeze_environment": "python -m pip freeze > requirements.txt",
    "install_from_requirements": "python -m pip install -r requirements.txt",
}


def dependency_workflow() -> list[str]:
    """Return the recommended dependency-management sequence."""

    return [
        "Create an isolated virtual environment.",
        "Upgrade pip in the active environment.",
        "Install only the dependencies the project needs.",
        "Record dependencies in a reproducible project file.",
        "Recreate the environment from that file on another machine.",
    ]


def packaging_principles() -> dict[str, str]:
    """Summarize the role of common Python packaging concepts."""

    return {
        "virtual_environment": "Isolates project dependencies from the system interpreter.",
        "package": "A reusable unit of Python code with an importable structure.",
        "pyproject.toml": "Modern configuration entry point for Python packaging and tools.",
        "requirements.txt": "A simple pinned dependency snapshot commonly used for deployments.",
        "dependency_locking": "Keeps dependency versions predictable across environments.",
    }


if __name__ == "__main__":
    print(PROJECT_SETUP)
    print(dependency_workflow())
    print(packaging_principles())
