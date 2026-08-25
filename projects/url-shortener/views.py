"""
Day 24 — URL Shortener DRF ViewSet, permissions, validation and responses.
Day 25 adds Django authentication and owner-scoped access.
"""

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
    permission_classes = [permissions.IsAuthenticated]
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
