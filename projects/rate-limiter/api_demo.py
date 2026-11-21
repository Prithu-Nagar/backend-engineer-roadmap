"""Run a small Flask API protected by the in-process token bucket."""

from flask import Flask, jsonify
from flask_middleware import register_rate_limit
from token_bucket import TokenBucketRateLimiter


def create_app(limiter=None):
    app = Flask(__name__)
    limiter = limiter or TokenBucketRateLimiter(capacity=5, refill_rate=1)

    # Demo identity only. Replace with an authenticated principal in a real API.
    register_rate_limit(
        app,
        limiter,
        key_func=lambda incoming_request: incoming_request.headers.get(
            "X-Client-ID", incoming_request.remote_addr or "anonymous"
        ),
    )

    @app.get("/resource")
    def resource():
        return jsonify(message="Request allowed")

    return app


if __name__ == "__main__":
    create_app().run(debug=False)
