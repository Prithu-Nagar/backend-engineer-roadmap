"""Django application configuration for the URL Shortener."""

from pathlib import Path

from django.apps import AppConfig


class URLShortenerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "url_shortener"
    path = str(Path(__file__).resolve().parent)
