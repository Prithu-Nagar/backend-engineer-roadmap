"""Day 48 — Dependency and vulnerability management for Python services."""

from __future__ import annotations

import re
from pathlib import Path


EXACT_PIN_PATTERN = re.compile(r"^([A-Za-z0-9_.-]+)==([0-9][A-Za-z0-9_.-]*)$")


def parse_requirement_lines(requirements_text: str) -> list[str]:
    """Return active requirement lines while ignoring comments and blanks."""
    requirements: list[str] = []

    for raw_line in requirements_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        requirements.append(line)

    return requirements


def is_exactly_pinned(requirement: str) -> bool:
    """Return whether a requirement uses an exact == version pin."""
    return bool(EXACT_PIN_PATTERN.fullmatch(requirement))


def unpinned_requirements(requirements_text: str) -> list[str]:
    """Return active dependencies that are not exactly version-pinned."""
    return [
        requirement
        for requirement in parse_requirement_lines(requirements_text)
        if not is_exactly_pinned(requirement)
    ]


def dependency_audit_command(requirements_path: str = "python/requirements.txt") -> list[str]:
    """Build the recommended pip-audit command for the pinned dependency set."""
    return [
        "python",
        "-m",
        "pip_audit",
        "-r",
        requirements_path,
    ]


def read_requirements(path: str | Path = "python/requirements.txt") -> str:
    """Read a requirements file for local validation or CI checks."""
    return Path(path).read_text(encoding="utf-8")


if __name__ == "__main__":
    requirements = read_requirements()
    unpinned = unpinned_requirements(requirements)

    if unpinned:
        print("Unpinned requirements:")
        for requirement in unpinned:
            print(f"- {requirement}")
    else:
        print("All active requirements are exactly pinned.")

    print("Audit command:", " ".join(dependency_audit_command()))
