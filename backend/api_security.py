"""Day 47 — API security helpers for validation, secrets, CORS, and CSRF."""

from __future__ import annotations

from collections.abc import Iterable

from flask import Request, Response


SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


def validate_origin(origin: str | None, allowed_origins: Iterable[str]) -> bool:
    """Return whether a request Origin is explicitly allow-listed."""
    if origin is None:
        return True
    return origin in set(allowed_origins)


def apply_cors_headers(
    response: Response,
    origin: str | None,
    allowed_origins: Iterable[str],
) -> Response:
    """Add narrow CORS headers only for an explicitly allowed origin."""
    if origin and validate_origin(origin, allowed_origins):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-CSRF-Token"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    return response


def csrf_required(request: Request, cookie_authenticated: bool) -> bool:
    """Return whether a state-changing cookie-authenticated request needs CSRF."""
    return cookie_authenticated and request.method not in SAFE_METHODS


def validate_csrf_token(
    request_token: str | None,
    session_token: str | None,
) -> bool:
    """Validate a CSRF token pair; token values must never be logged."""
    if not request_token or not session_token:
        return False
    return request_token == session_token


def add_security_headers(response: Response) -> Response:
    """Apply baseline browser-facing security headers."""
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response
