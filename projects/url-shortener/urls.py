"""
Day 23 — URL Shortener DRF URL configuration.
"""

from django.urls import path

from .views import ShortURLDetailView, ShortURLListCreateView


urlpatterns = [
    path("api/urls/", ShortURLListCreateView.as_view(), name="url-list-create"),
    path(
        "api/urls/<str:short_code>/",
        ShortURLDetailView.as_view(),
        name="url-detail",
    ),
]
