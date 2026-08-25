"""
Day 24 — URL Shortener DRF router configuration.
Day 25 keeps the router and applies authentication/ownership in the ViewSet.
"""

from rest_framework.routers import DefaultRouter

from .views import ShortURLViewSet


router = DefaultRouter()
router.register("api/urls", ShortURLViewSet, basename="url")

urlpatterns = router.urls
