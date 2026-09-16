"""Day 47 — Task Manager security hardening helpers."""

from __future__ import annotations

import hmac
import os
from collections.abc import Iterable


SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


def allowed_origins() -> tuple[str, ...]:
    """Return the configured CORS allow-list without permitting wildcard access."""
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "")
    return tuple(origin.strip() for origin in raw.split(",") if origin.strip())


def is_allowed_origin(origin: str | None, origins: Iterable[str] | None = None) -> bool:
    """Check an Origin against an explicit allow-list."""
    if origin is None:
        return True
    return origin in set(origins if origins is not None else allowed_origins())


def csrf_required(method: str, cookie_authenticated: bool) -> bool:
    """Return whether a state-changing cookie-authenticated request needs CSRF."""
    return cookie_authenticated and method.upper() not in SAFE_METHODS


def valid_csrf_token(request_token: str | None, session_token: str | None) -> bool:
    """Compare CSRF tokens without logging or normalizing secret values."""
    if not request_token or not session_token:
        return False
    return hmac.compare_digest(request_token, session_token)


def require_production_secret(secret: str | None, name: str = "SECRET_KEY") -> str:
    """Reject missing secrets when running in a production-like environment."""
    if os.getenv("APP_ENV", "development").lower() == "production":
        if not secret or not secret.strip():
            raise RuntimeError(f"{name} must be configured in production")
    return secret or ""


def security_headers() -> dict[str, str]:
    """Return baseline response headers for browser-facing API responses."""
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
