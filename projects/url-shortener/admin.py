"""
Django admin registration for the URL Shortener model.

Day 25 exposes ownership information so administrators can inspect and manage
authenticated users' short URLs.
"""

from django.contrib import admin

from .models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = (
        "short_code",
        "owner",
        "original_url",
        "created_at",
        "expires_at",
        "is_active",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("short_code", "original_url", "owner__username", "owner__email")
    autocomplete_fields = ("owner",)
