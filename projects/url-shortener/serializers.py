"""
Day 23 — URL Shortener DRF serializers.
"""

from rest_framework import serializers

from .models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = (
            "short_code",
            "short_url",
            "original_url",
            "created_at",
            "expires_at",
            "is_active",
        )
        read_only_fields = ("short_code", "created_at", "short_url")

    def get_short_url(self, obj: ShortURL) -> str:
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(f"/{obj.short_code}")
        return f"/{obj.short_code}"
