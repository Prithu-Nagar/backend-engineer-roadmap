"""
Task Manager API

Main Flask application entry point.
"""

from flask import Flask

from config import Config
from flask_routing import task_bp
from pagination import pagination_bp
from monitoring_health_checks import health_bp


def create_app():
    """Create and configure the Flask application."""

    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(task_bp)
    app.register_blueprint(pagination_bp)
    app.register_blueprint(health_bp)

    @app.route("/")
    def home():
        return {
            "message": "Task Manager API"
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)