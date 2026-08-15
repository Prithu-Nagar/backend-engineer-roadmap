"""
Shared pytest fixtures for the Task Manager test suite.

Day 15 focus:
- Reusable fixtures
- Test data
- Authentication data
- Task data
"""

import pytest


@pytest.fixture
def user_data():
    """Regular authenticated user."""
    return {
        "user_id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "user",
    }


@pytest.fixture
def admin_data():
    """Administrator user."""
    return {
        "user_id": 99,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
    }


@pytest.fixture
def other_user_data():
    """Second regular user used for ownership tests."""
    return {
        "user_id": 2,
        "username": "otheruser",
        "email": "other@example.com",
        "role": "user",
    }


@pytest.fixture
def task_data():
    """Task owned by the primary test user."""
    return {
        "task_id": 1,
        "user_id": 1,
        "title": "Complete backend refactoring",
        "description": "Refactor the authentication module",
        "status": "in_progress",
        "priority": "high",
    }


@pytest.fixture
def other_user_task():
    """Task owned by another user."""
    return {
        "task_id": 2,
        "user_id": 2,
        "title": "Other user's task",
        "description": "Task owned by another user",
        "status": "pending",
        "priority": "medium",
    }


@pytest.fixture
def multiple_tasks():
    """Multiple tasks for filtering and collection tests."""
    return [
        {
            "task_id": 1,
            "user_id": 1,
            "title": "Task 1",
            "status": "completed",
        },
        {
            "task_id": 2,
            "user_id": 1,
            "title": "Task 2",
            "status": "in_progress",
        },
        {
            "task_id": 3,
            "user_id": 2,
            "title": "Task 3",
            "status": "pending",
        },
    ]