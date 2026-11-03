"""Environment-based Flask and database configuration."""

import os
from typing import ClassVar


def _database_uri(value: str) -> str:
    """Use psycopg 3 explicitly for PostgreSQL connection URLs."""
    if value.startswith("postgres://"):
        return value.replace("postgres://", "postgresql+psycopg://", 1)
    if value.startswith("postgresql://"):
        return value.replace("postgresql://", "postgresql+psycopg://", 1)
    return value


def _env_bool(name: str, default: bool = False) -> bool:
    """Parse a boolean environment variable."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    """Base application configuration."""

    ENVIRONMENT = os.getenv("APP_ENV", "development").strip().lower()
    DEBUG = _env_bool("APP_DEBUG", default=ENVIRONMENT == "development")
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-secret")
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_DATABASE_URI = _database_uri(DATABASE_URL) or "sqlite:///task_manager.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict[str, bool]] = {"pool_pre_ping": True}
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class TestingConfig(Config):
    """Isolated in-memory database configuration for tests."""

    ENVIRONMENT = "testing"
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict[str, bool]] = {}


class ProductionConfig(Config):
    """Production configuration with mandatory external secrets and database."""

    ENVIRONMENT = "production"
    DEBUG = False
    TESTING = False

    @classmethod
    def validate(cls) -> None:
        """Fail fast when production-critical configuration is missing."""
        if not cls.DATABASE_URL:
            raise RuntimeError("DATABASE_URL must be configured in production")
        if cls.SECRET_KEY == "development-only-secret":
            raise RuntimeError("SECRET_KEY must be configured in production")
