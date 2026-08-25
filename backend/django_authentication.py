"""
Day 25 — Django Authentication, Sessions & Permissions

A compact reference for the authentication flow used by Django applications.
The examples use Django's built-in authentication system rather than storing
passwords or session identifiers manually.
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required


def authenticate_user(request, username: str, password: str):
    """Authenticate credentials and return the user or None."""

    return authenticate(request, username=username, password=password)


def login_user(request, username: str, password: str) -> bool:
    """Authenticate a user and create a Django session when valid."""

    user = authenticate_user(request, username, password)
    if user is None:
        return False

    login(request, user)
    return True


def logout_user(request) -> None:
    """Clear the authenticated user's session."""

    logout(request)


@login_required
def authenticated_view(request):
    """Example view boundary requiring an authenticated user."""

    return {"username": request.user.get_username()}


@permission_required("url_shortener.change_shorturl", raise_exception=True)
def manage_short_url(request):
    """Example permission boundary for a protected project operation."""

    return {"allowed": True}
