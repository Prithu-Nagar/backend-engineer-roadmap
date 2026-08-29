"""
URL Shortener FastAPI API tests.

Day 29 focus:
- FastAPI TestClient
- Request validation
- Response models
- Dependency overrides
- Success and error responses
"""

from __future__ import annotations


def test_create_short_url(client):
    response = client.post(
        "/api/urls",
        json={"original_url": "https://example.com/articles/backend"},
    )

    assert response.status_code == 201

    body = response.json()
    assert len(body["short_code"]) == 6
    assert body["original_url"] == "https://example.com/articles/backend"
    assert body["short_url"].endswith(body["short_code"])


def test_create_short_url_rejects_invalid_url(client):
    response = client.post(
        "/api/urls",
        json={"original_url": "not-a-url"},
    )

    assert response.status_code == 422


def test_list_short_urls_uses_overridden_store(client, store):
    store["abc123"] = {
        "short_code": "abc123",
        "short_url": "http://localhost:8000/abc123",
        "original_url": "https://example.com",
    }

    response = client.get("/api/urls")

    assert response.status_code == 200
    assert response.json()[0]["short_code"] == "abc123"


def test_get_short_url(client, store):
    store["abc123"] = {
        "short_code": "abc123",
        "short_url": "http://localhost:8000/abc123",
        "original_url": "https://example.com",
    }

    response = client.get("/abc123")

    assert response.status_code == 200
    assert response.json()["original_url"] == "https://example.com/"


def test_get_missing_short_url_returns_404(client):
    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json()["detail"] == "Short URL not found."
