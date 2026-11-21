"""Flask integration for the token-bucket rate limiters."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any

from flask import Flask, g, jsonify, request


def register_rate_limit(
    app: Flask,
    limiter: Any,
    key_func: Callable[[Any], str],
    *,
    fail_open: bool = False,
) -> None:
    """Register global Flask rate-limit hooks.

    ``key_func`` should return a stable, trusted identity (for example an
    authenticated user or API-key identifier). Do not use an untrusted
    ``X-Forwarded-For`` value unless a trusted proxy has normalized it.

    When the limiter backend raises, ``fail_open=True`` allows the request and
    marks the response; the default fails closed with HTTP 503.
    """
    if not isinstance(app, Flask):
        raise TypeError("app must be a Flask application")
    if not callable(getattr(limiter, "allow", None)):
        raise TypeError("limiter must provide an allow method")
    if not callable(key_func):
        raise TypeError("key_func must be callable")

    @app.before_request
    def enforce_rate_limit():
        try:
            key = key_func(request)
            decision = limiter.allow(key)
        except Exception:
            app.logger.exception("Rate limiter decision failed")
            g.rate_limit_unavailable = True
            if fail_open:
                return None
            return jsonify(error="rate_limiter_unavailable"), 503

        g.rate_limit_decision = decision
        if not decision.allowed:
            retry_after = max(1, math.ceil(decision.retry_after))
            response = jsonify(
                error="rate_limit_exceeded",
                message="Request rate limit exceeded.",
                retry_after=retry_after,
            )
            response.status_code = 429
            response.headers["Retry-After"] = str(retry_after)
            return response
        return None

    @app.after_request
    def add_rate_limit_headers(response):
        decision = getattr(g, "rate_limit_decision", None)
        if decision is not None:
            response.headers["X-RateLimit-Limit"] = _header_number(decision.limit)
            response.headers["X-RateLimit-Remaining"] = _header_number(
                decision.remaining
            )
        if getattr(g, "rate_limit_unavailable", False):
            response.headers["X-RateLimit-Status"] = "unavailable"
        return response


def _header_number(value: float) -> str:
    """Format numeric quota values without unnecessary trailing zeroes."""
    return str(int(value)) if float(value).is_integer() else str(value)
