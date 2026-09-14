"""WSGI entry point for production Flask servers such as Gunicorn."""

from app import app

__all__ = ["app"]
