"""
Persistent Django/DRF URL creation tests.

These tests exercise the canonical implementation against a migrated
SQLite database rather than the in-memory FastAPI comparison store.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.test import APIClient
from url_shortener.models import ShortURL


@pytest.fixture
def api_client(django_database):
    user = get_user_model().objects.create_user(
        username="url-owner",
        password="test-password",
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_create_url_persists_record_and_assigns_owner(api_client):
    response = api_client.post(
        "/api/urls/",
        {"original_url": "https://example.com/articles/backend"},
        format="json",
    )

    assert response.status_code == 201
    payload = response.json()["data"]
    record = ShortURL.objects.get(short_code=payload["short_code"])

    assert record.original_url == "https://example.com/articles/backend"
    assert record.owner_id is not None
    assert payload["short_url"].endswith(record.short_code)


@pytest.mark.parametrize(
    "original_url",
    [
        "",
        "not-a-url",
        "ftp://example.com/file",
        "https:///missing-host",
    ],
)
def test_create_url_rejects_invalid_destination(api_client, original_url):
    response = api_client.post(
        "/api/urls/",
        {"original_url": original_url},
        format="json",
    )

    assert response.status_code == 400
    assert ShortURL.objects.count() == 0


def test_create_url_normalizes_surrounding_whitespace(api_client):
    response = api_client.post(
        "/api/urls/",
        {"original_url": "  https://example.com/path  "},
        format="json",
    )

    assert response.status_code == 201
    assert ShortURL.objects.get().original_url == "https://example.com/path"


def test_generated_code_collision_retries_against_database(api_client):
    ShortURL.objects.create(
        short_code="aaaaaa",
        original_url="https://existing.example",
    )

    choices = iter(["a"] * 6 + ["b"] * 6)
    with patch(
        "url_shortener.serializers.secrets.choice",
        side_effect=lambda _: next(choices),
    ):
        response = api_client.post(
            "/api/urls/",
            {"original_url": "https://new.example"},
            format="json",
        )

    assert response.status_code == 201
    assert response.json()["data"]["short_code"] == "bbbbbb"
    assert ShortURL.objects.count() == 2


def test_database_unique_constraint_rejects_duplicate_codes():
    ShortURL.objects.create(
        short_code="unique1",
        original_url="https://one.example",
    )

    with pytest.raises(IntegrityError):
        ShortURL.objects.create(
            short_code="unique1",
            original_url="https://two.example",
        )


def test_create_url_requires_authentication():
    response = APIClient().post(
        "/api/urls/",
        {"original_url": "https://example.com"},
        format="json",
    )

    assert response.status_code in {401, 403}
