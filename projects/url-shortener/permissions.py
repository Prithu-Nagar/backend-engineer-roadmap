"""
Day 25 — URL Shortener ownership permission.
"""

from rest_framework import permissions


class IsShortURLOwner(permissions.BasePermission):
    """Allow access only when the authenticated user owns the URL."""

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.owner_id == request.user.id
