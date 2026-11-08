"""
Day 24 — URL Shortener DRF ViewSet, permissions, validation and responses.
Day 25 adds Django authentication and owner-scoped access.
"""

from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from .models import ShortURL
from .permissions import IsShortURLOwner
from .serializers import ShortURLSerializer


class ShortURLViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Expose the URL Shortener through a router-friendly ViewSet."""

    serializer_class = ShortURLSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "short_code"

    def get_queryset(self):
        return ShortURL.objects.filter(
            owner=self.request.user,
            is_active=True,
        ).order_by("-created_at")

    def get_permissions(self):
        if self.action in {"retrieve"}:
            return [permission() for permission in self.permission_classes] + [
                IsShortURLOwner()
            ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner=request.user)
        output = self.get_serializer(instance)

        return Response(
            {"data": output.data},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "data": serializer.data,
                "meta": {"count": queryset.count()},
            }
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data})


def redirect_short_url(request, short_code):
    """Redirect active short URLs and atomically record successful visits."""
    del request
    short_url = get_object_or_404(ShortURL, short_code=short_code)

    if not short_url.is_active or (
        short_url.expires_at is not None and short_url.expires_at <= timezone.now()
    ):
        return HttpResponse(
            "This short URL is no longer available.",
            status=status.HTTP_410_GONE,
        )

    ShortURL.objects.filter(pk=short_url.pk).update(click_count=F("click_count") + 1)
    return HttpResponseRedirect(short_url.original_url)
