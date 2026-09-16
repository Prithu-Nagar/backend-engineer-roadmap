"""Day 47 — Security fundamentals for Python services."""

from __future__ import annotations

import hashlib
import hmac
import secrets


def generate_token_urlsafe(length: int = 32) -> str:
    """Generate a cryptographically secure URL-safe token."""
    if length <= 0:
        raise ValueError("length must be positive")
    return secrets.token_urlsafe(length)


def hash_identifier(value: str) -> str:
    """Create a one-way SHA-256 digest for non-secret identifiers."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def secure_compare(left: str, right: str) -> bool:
    """Compare security-sensitive strings without ordinary timing shortcuts."""
    return hmac.compare_digest(left.encode("utf-8"), right.encode("utf-8"))


def require_secret(secret: str | None, name: str = "SECRET_KEY") -> str:
    """Require a non-empty deployment secret instead of silently using a default."""
    if not secret or not secret.strip():
        raise RuntimeError(f"{name} must be supplied through deployment configuration")
    return secret


if __name__ == "__main__":
    token = generate_token_urlsafe()
    print("Generated token length:", len(token))
    print("Identifier digest:", hash_identifier("example-id"))
    print("Constant-time comparison:", secure_compare(token, token))
