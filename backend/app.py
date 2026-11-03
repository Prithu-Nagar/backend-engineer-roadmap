"""Task Manager Flask application factory and WSGI entry point."""

from pathlib import Path

from flask import Flask

if __package__:
    from . import models
    from .config import Config, ProductionConfig, TestingConfig
    from .extensions import db, migrate
    from .flask_routing import task_bp
    from .monitoring_health_checks import health_bp
    from .pagination import pagination_bp
else:  # pragma: no cover - Docker runs app.py as a top-level module
    import models  # noqa: F401
    from config import Config, ProductionConfig, TestingConfig
    from extensions import db, migrate
    from flask_routing import task_bp
    from monitoring_health_checks import health_bp
    from pagination import pagination_bp

def create_app(config_object: type[Config] | object | None = None) -> Flask:
    """Create an application with environment-specific database wiring."""
    app = Flask(__name__)
    selected_config = config_object or _config_from_environment()
    app.config.from_object(selected_config)

    if app.config.get("ENVIRONMENT") == "production":
        selected_config.validate()

    db.init_app(app)
    migration_directory = Path(__file__).resolve().parent.parent / "migrations"
    migrate.init_app(app, db, directory=str(migration_directory))
    app.register_blueprint(task_bp)
    app.register_blueprint(pagination_bp)
    app.register_blueprint(health_bp)

    @app.get("/")
    def home():
        return {"message": "Task Manager API"}

    @app.get("/health/database")
    def database_health():
        """Return database connectivity without exposing connection details."""
        from sqlalchemy import text

        db.session.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}

    return app


def _config_from_environment() -> type[Config]:
    """Choose a configuration class from APP_ENV."""
    import os

    environment = os.getenv("APP_ENV", "development").strip().lower()
    if environment == "testing":
        return TestingConfig
    if environment == "production":
        return ProductionConfig
    return Config


app = create_app()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
