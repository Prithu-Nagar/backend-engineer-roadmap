"""Runtime settings for the canonical Django/DRF URL Shortener."""

import os
from pathlib import Path
from urllib.parse import unquote, urlparse

BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = os.environ.get("SECRET_KEY", "local-development-only-change-me")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS", "localhost,127.0.0.1,testserver"
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "rest_framework",
    "url_shortener.apps.URLShortenerConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = "url_shortener.urls"
WSGI_APPLICATION = "url_shortener.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
TIME_ZONE = "UTC"


def _database_config():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }

    parsed = urlparse(database_url)
    if parsed.scheme not in {"postgres", "postgresql"}:
        raise ValueError("DATABASE_URL must use postgres:// or postgresql://.")

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": unquote(parsed.path.lstrip("/")),
        "USER": unquote(parsed.username or ""),
        "PASSWORD": unquote(parsed.password or ""),
        "HOST": parsed.hostname or "localhost",
        "PORT": str(parsed.port or 5432),
        "CONN_MAX_AGE": 60,
    }


DATABASES = {"default": _database_config()}

REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
            "TIMEOUT": 300,
        }
    }

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "url_create": os.environ.get("URL_CREATE_RATE", "10/hour"),
        "url_redirect": os.environ.get("URL_REDIRECT_RATE", "60/minute"),
    },
}
