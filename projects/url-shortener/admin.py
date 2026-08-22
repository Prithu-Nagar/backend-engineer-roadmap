"""
Django admin registration for the URL Shortener model.
"""

from django.contrib import admin

from .models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = (
        "short_code",
        "original_url",
        "created_at",
        "expires_at",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("short_code", "original_url")
