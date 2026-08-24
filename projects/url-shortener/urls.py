"""
Day 24 — URL Shortener DRF router configuration.
"""

from rest_framework.routers import DefaultRouter

from .views import ShortURLViewSet


router = DefaultRouter()
router.register("api/urls", ShortURLViewSet, basename="url")

urlpatterns = router.urls
