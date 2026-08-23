"""
Day 23 — URL Shortener DRF endpoints.
"""

from rest_framework import generics

from .models import ShortURL
from .serializers import ShortURLSerializer


class ShortURLListCreateView(generics.ListCreateAPIView):
    """List active short URLs and create a new short URL."""

    queryset = ShortURL.objects.filter(is_active=True)
    serializer_class = ShortURLSerializer


class ShortURLDetailView(generics.RetrieveAPIView):
    """Return metadata for a single active short URL."""

    queryset = ShortURL.objects.filter(is_active=True)
    serializer_class = ShortURLSerializer
    lookup_field = "short_code"
