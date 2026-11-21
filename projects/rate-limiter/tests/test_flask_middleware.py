"""HTTP contract and backend-failure tests for Flask rate limiting."""

import sys
from pathlib import Path

import pytest

flask = pytest.importorskip("flask")
Flask = flask.Flask
jsonify = flask.jsonify

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from flask_middleware import register_rate_limit
from token_bucket import TokenBucketRateLimiter


class BrokenLimiter:
    def allow(self, key):
        raise ConnectionError("Redis is unavailable")


@pytest.fixture
def app():
    application = Flask(__name__)
    limiter = TokenBucketRateLimiter(
        capacity=1, refill_rate=0.01, clock=lambda: 0.0
    )
    register_rate_limit(
        application,
        limiter,
        key_func=lambda request: request.headers.get("X-Client-ID", "anonymous"),
    )

    @application.get("/resource")
    def resource():
        return jsonify(message="ok")

    return application


def test_allowed_response_includes_quota_headers(app):
    response = app.test_client().get("/resource", headers={"X-Client-ID": "user-1"})

    assert response.status_code == 200
    assert response.headers["X-RateLimit-Limit"] == "1"
    assert response.headers["X-RateLimit-Remaining"] == "0"


def test_rejected_response_has_429_and_retry_headers(app):
    client = app.test_client()
    headers = {"X-Client-ID": "user-2"}
    assert client.get("/resource", headers=headers).status_code == 200

    response = client.get("/resource", headers=headers)
    assert response.status_code == 429
    assert response.json["error"] == "rate_limit_exceeded"
    assert int(response.headers["Retry-After"]) == response.json["retry_after"]
    assert response.headers["X-RateLimit-Remaining"] == "0"


def test_limiter_backend_failure_fails_closed_with_503():
    application = Flask(__name__)
    register_rate_limit(
        application, BrokenLimiter(), key_func=lambda request: "client"
    )
    application.add_url_rule("/resource", view_func=lambda: "ok")

    response = application.test_client().get("/resource")
    assert response.status_code == 503
    assert response.json == {"error": "rate_limiter_unavailable"}


def test_limiter_backend_failure_can_fail_open_explicitly():
    application = Flask(__name__)
    register_rate_limit(
        application,
        BrokenLimiter(),
        key_func=lambda request: "client",
        fail_open=True,
    )
    application.add_url_rule("/resource", view_func=lambda: "ok")

    response = application.test_client().get("/resource")
    assert response.status_code == 200
    assert response.headers["X-RateLimit-Status"] == "unavailable"


def test_invalid_middleware_configuration_is_rejected():
    application = Flask(__name__)
    with pytest.raises(TypeError, match="limiter"):
        register_rate_limit(application, object(), key_func=lambda request: "x")
