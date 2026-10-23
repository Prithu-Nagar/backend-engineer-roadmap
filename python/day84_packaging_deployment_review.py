"""Day 84 — Python packaging and deployment review."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path


def validate_required_environment(
    required: tuple[str, ...], environ: dict[str, str] | None = None
) -> dict[str, str]:
    """Return required configuration values or raise a useful error."""
    values = os.environ if environ is None else environ
    missing = [name for name in required if not values.get(name)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    return {name: values[name] for name in required}


def verify_runtime(expected_major: int, expected_minor: int) -> None:
    """Fail early when the active interpreter differs from the deployment target."""
    if (sys.version_info.major, sys.version_info.minor) != (
        expected_major, expected_minor
    ):
        raise RuntimeError(
            f"Expected Python {expected_major}.{expected_minor}; "
            f"running {sys.version_info.major}.{sys.version_info.minor}"
        )


def find_project_root(start: Path) -> Path:
    """Find a directory containing pyproject.toml or .git."""
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() or (candidate / ".git").exists():
            return candidate
    raise FileNotFoundError("Could not find project root")


def run_smoke_tests() -> None:
    assert validate_required_environment(
        ("APP_ENV", "DATABASE_URL"),
        {"APP_ENV": "test", "DATABASE_URL": "sqlite:///:memory:"},
    ) == {"APP_ENV": "test", "DATABASE_URL": "sqlite:///:memory:"}
    try:
        validate_required_environment(("SECRET_KEY",), {})
    except ValueError as exc:
        assert "SECRET_KEY" in str(exc)
    else:
        raise AssertionError("Missing configuration should fail fast")
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        (root / "pyproject.toml").write_text(
            '[project]\nname = "review"\n', encoding="utf-8"
        )
        assert find_project_root(root / "src").resolve() == root.resolve()


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 84 packaging/deployment review checks passed.")
