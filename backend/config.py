"""
Day 20 — Flask Configuration

Configuration is separated from application creation so that the same
application factory can be used with different environments.
"""


class Config:
    """Base application configuration."""

    ENVIRONMENT = "development"
    DEBUG = True
    TESTING = False


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