"""
Day 29 — FastAPI API Testing

Demonstrates:
- FastAPI TestClient
- Endpoint assertions
- Dependency overrides
- Isolated test state
- Testing validation and error responses

The project-level URL Shortener tests apply the same patterns to the actual
project FastAPI application.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


app = FastAPI(title="FastAPI Testing Example")


def get_items() -> list[str]:
    """Return the default dependency value."""
    return ["production-item"]


@app.get("/items")
def list_items(items: list[str] = Depends(get_items)) -> dict[str, list[str]]:
    """Return dependency-provided items."""
    return {"items": items}


def test_dependency_override() -> None:
    """Replace a dependency with deterministic test data."""
    app.dependency_overrides[get_items] = lambda: ["test-item"]

    with TestClient(app) as client:
        response = client.get("/items")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"items": ["test-item"]}


if __name__ == "__main__":
    test_dependency_override()
    print("FastAPI dependency override test passed.")
