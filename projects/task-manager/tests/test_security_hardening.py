"""Tests for Day 47 Task Manager security hardening."""

from security_hardening import (
    is_allowed_origin,
    csrf_required,
    require_production_secret,
    security_headers,
    valid_csrf_token,
)


def test_cors_requires_explicit_origin_allow_list():
    assert is_allowed_origin("https://app.example.com", ["https://app.example.com"])
    assert not is_allowed_origin("https://evil.example", ["https://app.example.com"])


def test_csrf_is_required_for_state_changing_cookie_requests():
    assert csrf_required("POST", True)
    assert not csrf_required("GET", True)
    assert not csrf_required("POST", False)


def test_csrf_token_comparison():
    assert valid_csrf_token("token", "token")
    assert not valid_csrf_token("token", "different")
    assert not valid_csrf_token(None, "token")


def test_production_secret_is_required(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")

    try:
        require_production_secret("")
    except RuntimeError as exc:
        assert "SECRET_KEY" in str(exc)
    else:
        raise AssertionError("Expected a missing production secret to fail")


def test_development_can_use_empty_secret_for_example_configuration(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    assert require_production_secret("") == ""


def test_security_headers_are_present():
    headers = security_headers()

    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
