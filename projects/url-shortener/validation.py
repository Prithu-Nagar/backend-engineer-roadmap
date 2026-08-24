"""
Day 24 — URL Shortener validation helpers.

The DRF serializer is the primary validation boundary. These small helpers
keep reusable domain checks explicit and easy to test independently.
"""

from urllib.parse import urlparse


MAX_URL_LENGTH = 2048


def normalize_url(value: str) -> str:
    """Strip surrounding whitespace from a URL string."""

    return value.strip()


def validate_url(value: str) -> str | None:
    """Return an error message when a URL is invalid."""

    if not isinstance(value, str):
        return "URL must be a string."

    value = normalize_url(value)

    if not value:
        return "URL is required."

    if len(value) > MAX_URL_LENGTH:
        return f"URL must not exceed {MAX_URL_LENGTH} characters."

    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "URL must include an http or https scheme and a host."

    return None
