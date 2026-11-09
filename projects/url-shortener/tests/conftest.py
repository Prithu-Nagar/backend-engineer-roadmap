"""
URL Shortener FastAPI test fixtures.

Day 29 focus:
- API testing
- Dependency overrides
- Isolated test state
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import django
import pytest
from django.conf import settings
from fastapi.testclient import TestClient

PROJECT_DIR = Path(__file__).resolve().parents[1]

# Configure a small SQLite-backed Django environment for the canonical
# persistent implementation tests. The FastAPI comparison tests remain
# isolated and continue using dependency overrides.

app_package = ModuleType("url_shortener")
app_package.__path__ = [str(PROJECT_DIR)]
sys.modules.setdefault("url_shortener", app_package)

if not settings.configured:
    settings.configure(
        SECRET_KEY="url-shortener-tests",
        DEBUG=True,
        ALLOWED_HOSTS=["testserver"],
        USE_TZ=True,
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        ROOT_URLCONF="url_shortener.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "rest_framework",
            "url_shortener",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        MIDDLEWARE=[],
        REST_FRAMEWORK={
            "DEFAULT_AUTHENTICATION_CLASSES": [
                "rest_framework.authentication.SessionAuthentication",
                "rest_framework.authentication.BasicAuthentication",
            ],
            "DEFAULT_PERMISSION_CLASSES": [
                "rest_framework.permissions.IsAuthenticated",
            ],
            "DEFAULT_THROTTLE_RATES": {
                "url_create": "2/hour",
                "url_redirect": "2/minute",
            },
        },
    )

django.setup()

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



@pytest.fixture(scope="session", autouse=True)
def django_database():
    """Create the migrated SQLite schema for Django API tests."""
    from django.core.management import call_command

    call_command("migrate", verbosity=0, interactive=False)



@pytest.fixture(autouse=True)
def clean_django_database(django_database):
    """Keep persistent API tests independent while reusing the migrated DB."""
    from django.core.management import call_command

    call_command("flush", verbosity=0, interactive=False)


@pytest.fixture(autouse=True)
def clear_throttle_cache():
    """Prevent rate-limit state from leaking between tests."""
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()
