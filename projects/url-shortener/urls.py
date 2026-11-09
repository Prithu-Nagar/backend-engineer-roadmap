"""
Day 24 — URL Shortener DRF router configuration.
Day 25 keeps the router and applies authentication/ownership in the ViewSet.
Day 8 adds the public short-code redirect route.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ShortURLViewSet, health_check, redirect_short_url

router = DefaultRouter()
router.register("api/urls", ShortURLViewSet, basename="url")

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("<str:short_code>", redirect_short_url, name="short-url-redirect"),
    *router.urls,
]
