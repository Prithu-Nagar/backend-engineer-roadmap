"""
Day 12 - Task Manager Authorization

Implements role-based authorization for the Task Manager API.

Authentication identifies the user.
Authorization determines what the authenticated user is allowed to do.
"""

from functools import wraps
from typing import Callable

from error_handling import (
    FORBIDDEN,
    UNAUTHORIZED,
    TaskManagerError,
)


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


def get_permissions(role: str) -> set[str]:
    """
    Return the permissions assigned to a role.
    """
    return ROLE_PERMISSIONS.get(role, set())


def has_permission(role: str, permission: str) -> bool:
    """
    Check whether a role has the requested permission.
    """
    return permission in get_permissions(role)


def requires_permission(permission: str) -> Callable:
    """
    Protect a function by requiring a specific permission.
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(user: dict, *args, **kwargs):
            if not user:
                return UNAUTHORIZED.to_response()

            role = user.get("role")

            return TaskManagerError(
                code="ROLE_NOT_FOUND",
                message="User role not found.",
                status_code=403,
            ).to_response()

            if not has_permission(role, permission):
                return FORBIDDEN.to_response()

            return function(user, *args, **kwargs)

        return wrapper

    return decorator


def can_access_task(user: dict, task: dict) -> bool:
    """
    Check whether a user can access a task.

    Administrators can access all tasks.
    Regular users can access only their own tasks.
    """
    if user.get("role") == "admin":
        return True

    return user.get("user_id") == task.get("user_id")


@requires_permission("create_task")
def create_task(user: dict, title: str) -> dict:
    """
    Create a task for the authenticated user.
    """
    return {
        "message": "Task created",
        "created_by": user["user_id"],
        "title": title,
    }


@requires_permission("read_task")
def read_task(user: dict, task: dict) -> dict:
    """
    Read a task after checking resource ownership.
    """
    if not can_access_task(user, task):
        return TaskManagerError(
            code="TASK_ACCESS_FORBIDDEN",
            message="You are not allowed to access this task.",
            status_code=403,
        ).to_response()

    return task


@requires_permission("update_task")
def update_task(user: dict, task: dict, title: str) -> dict:
    """
    Update a task after checking resource ownership.
    """
    if not can_access_task(user, task):
        return {
            "error": "You are not allowed to update this task"
        }, 403

    task["title"] = title

    return task


@requires_permission("delete_task")
def delete_task(user: dict, task: dict) -> dict:
    """
    Delete a task after checking resource ownership.
    """
    if not can_access_task(user, task):
        return {
            "error": "You are not allowed to delete this task"
        }, 403

    return {
        "message": "Task deleted",
        "task_id": task["task_id"],
    }


@requires_permission("manage_users")
def manage_users(user: dict) -> dict:
    """
    Administrative operation available only to admins.
    """
    return {
        "message": "User management access granted",
        "user": user["user_id"],
    }


if __name__ == "__main__":
    admin = {
        "user_id": 1,
        "username": "alice",
        "role": "admin",
    }

    user = {
        "user_id": 2,
        "username": "bob",
        "role": "user",
    }

    task = {
        "task_id": 101,
        "user_id": 2,
        "title": "Build Task Manager API",
    }

    print(create_task(user, "Write authorization layer"))
    print(read_task(user, task))
    print(update_task(user, task, "Implement RBAC"))
    print(delete_task(user, task))
    print(manage_users(admin))
    print(manage_users(user))