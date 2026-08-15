"""
Flask Testing

Day 15 focus:
- Flask testing
- Flask test client
- Pytest fixtures
- Request/response testing
- API integration tests
"""

import pytest
from flask import Flask, jsonify


def create_app() -> Flask:
    """Create a small Flask application for testing."""

    app = Flask(__name__)
    app.config["TESTING"] = True

    @app.route("/")
    def home():
        return jsonify({"message": "Welcome"})

    @app.route("/api/user/<int:user_id>")
    def get_user(user_id: int):
        return jsonify(
            {
                "id": user_id,
                "name": f"User {user_id}",
            }
        )

    @app.route("/api/data", methods=["POST"])
    def create_data():
        return jsonify({"status": "created"}), 201

    return app


@pytest.fixture
def client():
    """Create a Flask test client."""

    app = create_app()

    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home endpoint."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json == {"message": "Welcome"}


def test_get_user(client):
    """Test a dynamic route and JSON response."""

    response = client.get("/api/user/1")

    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json["name"] == "User 1"


def test_create_data(client):
    """Test a POST endpoint."""

    response = client.post("/api/data")

    assert response.status_code == 201
    assert response.json["status"] == "created"


def test_user_not_found(client):
    """Test Flask's default 404 response."""

    response = client.get("/api/user/not-a-number")

    assert response.status_code == 404


def test_unsupported_method(client):
    """Test HTTP method validation."""

    response = client.get("/api/data")

    assert response.status_code == 405