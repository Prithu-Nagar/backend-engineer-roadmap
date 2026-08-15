"""
Task Manager authentication and authorization tests.

Day 15 focus:
- JWT token creation
- JWT token decoding
- Role-based authorization
- Permission checks
- Authentication failures
"""

import importlib.util
from pathlib import Path

import pytest


TASK_MANAGER_DIR = Path(__file__).resolve().parents[1]


def load_module(module_name: str, filename: str):
    """Load a Task Manager module from its file path."""

    path = TASK_MANAGER_DIR / filename

    spec = importlib.util.spec_from_file_location(
        module_name,
        path,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


authorization = load_module(
    "task_manager_authorization",
    "authorization.py",
)

jwt_authentication = load_module(
    "task_manager_jwt_authentication",
    "jwt_authentication.py",
)


def test_user_has_expected_permissions(user_data):
    """Regular users have task permissions."""

    permissions = authorization.get_permissions(
        user_data["role"]
    )

    assert "create_task" in permissions
    assert "read_task" in permissions
    assert "update_task" in permissions
    assert "delete_task" in permissions


def test_user_cannot_manage_users(user_data):
    """Regular users cannot manage users."""

    assert authorization.has_permission(
        user_data["role"],
        "manage_users",
    ) is False


def test_admin_can_manage_users(admin_data):
    """Administrators can manage users."""

    assert authorization.has_permission(
        admin_data["role"],
        "manage_users",
    ) is True


def test_manage_users_requires_admin(user_data):
    """Regular users receive a permission error."""

    result = authorization.manage_users(user_data)

    assert result[1] == 403
    assert "permission" in result[0]["error"].lower()


def test_manage_users_allows_admin(admin_data):
    """Admins can access user-management functionality."""

    result = authorization.manage_users(admin_data)

    assert result["message"] == "User management access granted"
    assert result["user"] == admin_data["user_id"]


def test_missing_user_requires_authentication():
    """Missing user information returns 401."""

    result = authorization.create_task(
        None,
        "Test task",
    )

    assert result[1] == 401
    assert "authentication" in result[0]["error"].lower()


def test_missing_role_returns_forbidden():
    """Authenticated users without a role receive 403."""

    user = {
        "user_id": 10,
        "username": "norole",
    }

    result = authorization.create_task(
        user,
        "Test task",
    )

    assert result[1] == 403
    assert "role" in result[0]["error"].lower()


def test_create_access_token(user_data):
    """JWT access tokens can be created."""

    token = jwt_authentication.create_access_token(
        user_data["user_id"]
    )

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_access_token(user_data):
    """A valid JWT can be decoded."""

    token = jwt_authentication.create_access_token(
        user_data["user_id"]
    )

    payload = jwt_authentication.decode_access_token(token)

    assert payload["sub"] == str(user_data["user_id"])
    assert "iat" in payload
    assert "exp" in payload


def test_invalid_token_is_rejected():
    """An invalid JWT should fail validation."""

    with pytest.raises(Exception):
        jwt_authentication.decode_access_token(
            "invalid.token.value"
        )