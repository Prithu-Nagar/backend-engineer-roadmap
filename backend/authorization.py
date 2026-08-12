"""
Day 12 - Authorization

Topics:
- Authentication vs authorization
- Roles
- Permissions
- Role-Based Access Control (RBAC)
- Permission checks
"""

from functools import wraps
from typing import Callable


ROLE_PERMISSIONS = {
    "admin": {
        "create_task",
        "read_task",
        "update_task",
        "delete_task",
        "manage_users",
    },
    "user": {
        "create_task",
        "read_task",
        "update_task",
        "delete_task",
    },
}


def has_permission(role: str, permission: str) -> bool:
    """
    Check whether a role has the required permission.
    """
    return permission in ROLE_PERMISSIONS.get(role, set())


def requires_permission(permission: str) -> Callable:
    """
    Decorator for protecting a route or function with a permission check.
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(user: dict, *args, **kwargs):
            role = user.get("role")

            if not role:
                return {
                    "error": "Authentication required"
                }, 401

            if not has_permission(role, permission):
                return {
                    "error": "Forbidden"
                }, 403

            return function(user, *args, **kwargs)

        return wrapper

    return decorator


@requires_permission("read_task")
def read_tasks(user: dict) -> dict:
    return {
        "message": f"Tasks available for {user['username']}"
    }


@requires_permission("manage_users")
def manage_users(user: dict) -> dict:
    return {
        "message": f"User management available for {user['username']}"
    }


if __name__ == "__main__":
    admin_user = {
        "username": "alice",
        "role": "admin",
    }

    normal_user = {
        "username": "bob",
        "role": "user",
    }

    print(read_tasks(admin_user))
    print(read_tasks(normal_user))
    print(manage_users(admin_user))
    print(manage_users(normal_user))