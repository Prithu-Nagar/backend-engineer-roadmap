"""
Day 24 — URL Shortener DRF validation and API representation.
Day 25 adds authenticated ownership to the API representation.
"""

import secrets
import string
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import ShortURL
from .validation import validate_url


SHORT_CODE_ALPHABET = string.ascii_letters + string.digits
SHORT_CODE_LENGTH = 6
MAX_URL_LENGTH = 2048


class ShortURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ShortURL
        fields = (
            "short_code",
            "short_url",
            "original_url",
            "created_at",
            "expires_at",
            "is_active",
            "owner",
        )
        read_only_fields = (
            "short_code",
            "created_at",
            "short_url",
            "owner",
        )

    def validate_original_url(self, value: str) -> str:
        value = value.strip()
        error = validate_url(value)
        if error is not None:
            raise serializers.ValidationError(error)
        return value

    def validate_expires_at(self, value):
        if value is not None and value <= timezone.now():
            raise serializers.ValidationError(
                "expires_at must be in the future."
            )

        return value

    def validate(self, attrs):
        expires_at = attrs.get("expires_at")
        if expires_at is not None and expires_at > timezone.now() + timedelta(
            days=3650
        ):
            raise serializers.ValidationError(
                {"expires_at": "Expiration date is unreasonably far in the future."}
            )
        return attrs

    def create(self, validated_data):
        for _ in range(10):
            short_code = "".join(
                secrets.choice(SHORT_CODE_ALPHABET)
                for _ in range(SHORT_CODE_LENGTH)
            )
            if not ShortURL.objects.filter(short_code=short_code).exists():
                return ShortURL.objects.create(
                    short_code=short_code,
                    **validated_data,
                )

        raise serializers.ValidationError(
            {"short_code": "Unable to generate a unique short code."}
        )

    def get_short_url(self, obj: ShortURL) -> str:
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(f"/{obj.short_code}")
        return f"/{obj.short_code}"
