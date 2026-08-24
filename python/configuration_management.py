"""
Day 24 — Configuration Management, Environment Variables & Secrets

This module demonstrates a small, dependency-free configuration boundary for
backend applications. Secrets are read from the environment and are never
hard-coded into source code.
"""

from __future__ import annotations

import os


class ConfigurationError(RuntimeError):
    """Raised when required application configuration is missing."""


class Settings:
    """Load application configuration from environment variables."""

    def __init__(self) -> None:
        self.environment = os.getenv("APP_ENV", "development")
        self.debug = os.getenv("APP_DEBUG", "false").lower() == "true"
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
        self.secret_key = self._required_secret("APP_SECRET_KEY")

    @staticmethod
    def _required_secret(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise ConfigurationError(f"Required secret is missing: {name}")
        return value


def load_settings() -> Settings:
    """Create the application's configuration object."""

    return Settings()


if __name__ == "__main__":
    try:
        settings = load_settings()
    except ConfigurationError as exc:
        print(exc)
    else:
        print(f"Environment: {settings.environment}")
        print(f"Debug: {settings.debug}")
        print(f"Database configured: {bool(settings.database_url)}")
        print("Secret key loaded: yes")
