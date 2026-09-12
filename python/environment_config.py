"""Separate application configuration from environment-specific values."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    app_env: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///local.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def load_settings() -> Settings:
    """Create an immutable settings object for the current environment."""
    return Settings()


if __name__ == "__main__":
    settings = load_settings()
    print(f"environment={settings.app_env}")
    print(f"debug={settings.debug}")
    print(f"database={settings.database_url}")
    print(f"redis={settings.redis_url}")
