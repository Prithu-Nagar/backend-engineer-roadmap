"""
Day 45 — Application Configuration for Deployment

Keep deployment-specific values in the environment instead of hard-coding
secrets, hosts, and connection strings in application source code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DeploymentSettings:
    """Immutable runtime settings loaded from environment variables."""

    environment: str
    debug: bool
    host: str
    port: int
    database_url: str
    redis_url: str


def _as_bool(value: str, default: bool = False) -> bool:
    """Parse common environment boolean values."""
    normalized = value.strip().lower()
    if not normalized:
        return default
    return normalized in {"1", "true", "yes", "on"}


def load_settings() -> DeploymentSettings:
    """Load deployment settings from environment variables."""
    environment = os.getenv("APP_ENV", "development")
    debug = _as_bool(os.getenv("APP_DEBUG", "false"))

    if environment == "production" and debug:
        raise ValueError("APP_DEBUG must be false in production")

    return DeploymentSettings(
        environment=environment,
        debug=debug,
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "5000")),
        database_url=os.getenv("DATABASE_URL", ""),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    )


if __name__ == "__main__":
    print(load_settings())
