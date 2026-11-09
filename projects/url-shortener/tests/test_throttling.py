"""Abuse-safeguard tests for URL creation and public redirects."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient
from url_shortener.models import ShortURL


@pytest.fixture
def authenticated_client(django_database):
    user = get_user_model().objects.create_user(
        username="throttle-owner",
        password="test-password",
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_url_creation_is_throttled_per_authenticated_user(authenticated_client):
    payload = {"original_url": "https://example.com/resource"}

    first = authenticated_client.post("/api/urls/", payload, format="json")
    second = authenticated_client.post("/api/urls/", payload, format="json")

    assert first.status_code == 201
    assert second.status_code == 201
    response = authenticated_client.post("/api/urls/", payload, format="json")

    assert response.status_code == 429
    assert ShortURL.objects.count() == 2


def test_public_redirects_are_throttled_per_client_ip(django_database):
    record = ShortURL.objects.create(
        short_code="limit01",
        original_url="https://example.com/destination",
    )
    client = Client(REMOTE_ADDR="198.51.100.10")

    assert client.get("/limit01").status_code == 302
    assert client.get("/limit01").status_code == 302
    response = client.get("/limit01")

    assert response.status_code == 429
    record.refresh_from_db()
    assert record.click_count == 2


def test_health_endpoint_is_public():
    response = Client().get("/health/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
