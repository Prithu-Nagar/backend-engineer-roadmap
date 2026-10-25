"""Day 86 — Python security review helpers.

Examples focus on safe defaults and validation. Prefer maintained libraries
and framework protections for real applications.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from pathlib import Path


def constant_time_token_match(candidate: str | None, expected: str | None) -> bool:
    """Compare non-empty tokens without a timing-sensitive equality check."""
    if not candidate or not expected:
        return False
    return hmac.compare_digest(candidate, expected)


def generate_csrf_token() -> str:
    """Generate an unpredictable token suitable for a CSRF-token example."""
    return secrets.token_urlsafe(32)


def safe_child_path(root: str | Path, user_path: str) -> Path:
    """Resolve a user-supplied relative path and reject traversal outside root."""
    base = Path(root).resolve()
    candidate = (base / user_path).resolve()
    if candidate != base and base not in candidate.parents:
        raise ValueError("path escapes the configured root")
    return candidate


def sha256_fingerprint(value: bytes) -> str:
    """Return a non-secret fingerprint for integrity checks, not password storage."""
    return hashlib.sha256(value).hexdigest()


def run_smoke_tests() -> None:
    assert constant_time_token_match("same", "same")
    assert not constant_time_token_match("one", "two")
    assert not constant_time_token_match(None, "token")
    assert len(generate_csrf_token()) >= 32
    assert safe_child_path("/tmp/uploads", "report.txt") == Path("/tmp/uploads/report.txt")
    try:
        safe_child_path("/tmp/uploads", "../secrets.txt")
    except ValueError:
        pass
    else:
        raise AssertionError("path traversal must be rejected")
    assert sha256_fingerprint(b"data") == hashlib.sha256(b"data").hexdigest()


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 86 Python security review checks passed.")
