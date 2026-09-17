"""Day 48 — Dependency pinning and vulnerability scanning helpers."""

from __future__ import annotations

import re
from pathlib import Path


EXACT_REQUIREMENT = re.compile(r"^([A-Za-z0-9_.-]+)==([0-9][A-Za-z0-9_.-]*)$")


def dependency_names(requirements_text: str) -> list[str]:
    """Extract package names from active, exactly pinned requirements."""
    names: list[str] = []

    for raw_line in requirements_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = EXACT_REQUIREMENT.fullmatch(line)
        if match:
            names.append(match.group(1))
        else:
            raise ValueError(f"Requirement is not exactly pinned: {line}")

    return names


def validate_requirements_file(
    path: str | Path = "python/requirements.txt",
) -> list[str]:
    """Validate that every active dependency is pinned to an exact version."""
    requirements_text = Path(path).read_text(encoding="utf-8")
    return dependency_names(requirements_text)


def pip_audit_command(
    path: str = "python/requirements.txt",
) -> list[str]:
    """Return the CI command used to scan the pinned dependency set."""
    return ["python", "-m", "pip_audit", "-r", path]


if __name__ == "__main__":
    packages = validate_requirements_file()
    print(f"Validated {len(packages)} pinned dependencies.")
    print("Security scan:", " ".join(pip_audit_command()))
