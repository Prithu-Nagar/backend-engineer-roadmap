"""
Day 20 — Flask Configuration

Configuration is separated from application creation so that the same
application factory can be used with different environments.
"""

import os


def _env_bool(name: str, default: bool = False) -> bool:
    """Parse a boolean environment variable."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    """Base application configuration."""

    ENVIRONMENT = os.getenv("APP_ENV", "development")
    DEBUG = _env_bool("APP_DEBUG", default=ENVIRONMENT == "development")
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-secret")
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class TestingConfig(Config):
    """Configuration used when running tests."""

    ENVIRONMENT = "testing"
    DEBUG = False
    TESTING = True


class ProductionConfig(Config):
    """Configuration used for production deployments."""

    ENVIRONMENT = "production"
    DEBUG = False
    TESTING = False
