"""
Day 23 — Django REST Framework Fundamentals

A small DRF example showing the role of serializers in an API boundary.
The file is intentionally focused on the serializer layer rather than a
complete Django project configuration.
"""

from rest_framework import serializers


class ShortURLSerializer(serializers.Serializer):
    short_code = serializers.CharField(max_length=32, read_only=True)
    original_url = serializers.URLField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    is_active = serializers.BooleanField(default=True)

    def validate_original_url(self, value: str) -> str:
        """Normalize the URL value before it reaches application logic."""
        return value.strip()


class ShortURLSummarySerializer(serializers.Serializer):
    short_code = serializers.CharField()
    original_url = serializers.URLField()
    is_active = serializers.BooleanField()


def serializer_example() -> dict:
    """Return a validated representation for documentation/demo purposes."""

    serializer = ShortURLSerializer(
        data={
            "original_url": "https://example.com/backend",
            "is_active": True,
        }
    )
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


if __name__ == "__main__":
    print(serializer_example())
