"""
URL Shortener FastAPI test fixtures.

Day 29 focus:
- API testing
- Dependency overrides
- Isolated test state
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


PROJECT_DIR = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_DIR / "fastapi_app.py"

spec = importlib.util.spec_from_file_location("url_shortener_fastapi", APP_PATH)
assert spec is not None
assert spec.loader is not None

fastapi_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fastapi_app)


@pytest.fixture
def store():
    """Provide an isolated in-memory store for each test."""
    return {}


@pytest.fixture
def client(store):
    """Create a TestClient with the storage dependency overridden."""
    fastapi_app.app.dependency_overrides[fastapi_app.get_url_store] = (
        lambda: store
    )

    with TestClient(fastapi_app.app) as test_client:
        yield test_client

    fastapi_app.app.dependency_overrides.clear()
