"""
Day 24 — DRF ViewSets, Routers & Permissions

A compact example showing how Django REST Framework can move endpoint logic
into a ViewSet and let a router generate URL patterns.
"""

from rest_framework import permissions, serializers, viewsets
from rest_framework.response import Response


class ShortURLSerializer(serializers.Serializer):
    short_code = serializers.CharField(max_length=32, read_only=True)
    original_url = serializers.URLField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    is_active = serializers.BooleanField(default=True)

    def validate_original_url(self, value: str) -> str:
        return value.strip()


class ExampleShortURLViewSet(viewsets.ViewSet):
    """Illustrate ViewSet actions without requiring a project database."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        return Response({"data": [], "meta": {"count": 0}})

    def retrieve(self, request, pk=None):
        return Response(
            {
                "data": {
                    "short_code": pk,
                }
            }
        )


# In a Django project, the ViewSet is registered with a DRF router:
#
# router = DefaultRouter()
# router.register("urls", ExampleShortURLViewSet, basename="url")
# urlpatterns = router.urls


def serializer_example() -> dict:
    """Return validated data for a small standalone serializer example."""

    serializer = ShortURLSerializer(
        data={
            "original_url": "https://example.com/backend",
            "is_active": True,
        }
    )
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


if __name__ == "__main__":
    print(serializer_example())
