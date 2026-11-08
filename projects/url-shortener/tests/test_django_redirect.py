"""Redirect lifecycle and analytics tests for the Django URL Shortener."""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone
from rest_framework.test import APIClient
from url_shortener.models import ShortURL


@pytest.fixture
def owned_url(django_database):
    owner = get_user_model().objects.create_user(
        username="redirect-owner",
        password="test-password",
    )
    return ShortURL.objects.create(
        owner=owner,
        short_code="abc123",
        original_url="https://example.com/destination",
    )


@pytest.fixture
def django_client(django_database):
    return Client()


@pytest.fixture
def api_client(django_database):
    return APIClient()


def test_redirects_active_url_and_increments_click_count(django_client, owned_url):
    response = django_client.get("/abc123", follow=False)

    assert response.status_code == 302
    assert response["Location"] == "https://example.com/destination"
    owned_url.refresh_from_db()
    assert owned_url.click_count == 1


def test_each_successful_redirect_increments_analytics(django_client, owned_url):
    django_client.get("/abc123")
    django_client.get("/abc123")

    owned_url.refresh_from_db()
    assert owned_url.click_count == 2


def test_expired_url_returns_gone_without_incrementing_analytics(
    django_client, owned_url
):
    owned_url.expires_at = timezone.now() - timedelta(minutes=1)
    owned_url.save(update_fields=["expires_at"])

    response = django_client.get("/abc123")

    assert response.status_code == 410
    owned_url.refresh_from_db()
    assert owned_url.click_count == 0


def test_disabled_url_returns_gone_without_incrementing_analytics(
    django_client, owned_url
):
    owned_url.is_active = False
    owned_url.save(update_fields=["is_active"])

    response = django_client.get("/abc123")

    assert response.status_code == 410
    owned_url.refresh_from_db()
    assert owned_url.click_count == 0


def test_unknown_short_code_returns_not_found(django_client):
    response = django_client.get("/missing")

    assert response.status_code == 404


def test_url_metadata_exposes_click_analytics(api_client, owned_url):
    api_client.force_authenticate(user=owned_url.owner)
    api_client.get("/abc123")
    response = api_client.get("/api/urls/abc123/")

    assert response.status_code == 200
    assert response.json()["data"]["click_count"] == 1
