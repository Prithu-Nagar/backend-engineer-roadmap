"""Tests for Day 46 Task Manager health checks."""

from health_checks import liveness_check, readiness_check


def test_liveness_check_is_lightweight():
    body, status = liveness_check()

    assert status == 200
    assert body == {"status": "ok", "check": "liveness"}


def test_readiness_is_ok_when_dependencies_pass():
    body, status = readiness_check(
        database_check=lambda: None,
        redis_check=lambda: None,
    )

    assert status == 200
    assert body["status"] == "ok"
    assert body["dependencies"] == {
        "application": "ok",
        "database": "ok",
        "redis": "ok",
    }


def test_readiness_returns_503_when_dependency_fails():
    def failing_check():
        raise RuntimeError("database unavailable")

    body, status = readiness_check(database_check=failing_check)

    assert status == 503
    assert body["status"] == "not_ready"
    assert body["dependencies"]["database"] == "failed"
