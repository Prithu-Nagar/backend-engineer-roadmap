"""
URL Shortener Django model.

Day 22 introduces the first Django-backed project model.
Day 25 adds ownership so authenticated users can manage their own short URLs.
"""

from django.conf import settings
from django.db import models


class ShortURL(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="short_urls",
        null=True,
        blank=True,
    )
    short_code = models.CharField(max_length=32, unique=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.short_code
