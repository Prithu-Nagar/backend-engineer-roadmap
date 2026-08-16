"""
Task Manager - Day 16 Schemas

Defines the fields accepted by the API for task creation,
updates, and responses.
"""


CREATE_TASK_FIELDS = {
    "title",
    "description",
    "completed",
    "priority",
}

UPDATE_TASK_FIELDS = CREATE_TASK_FIELDS

RESPONSE_FIELDS = {
    "id",
    "title",
    "description",
    "completed",
    "priority",
    "created_at",
    "updated_at",
}


def create_task_schema(data):
    """Return only fields allowed during task creation."""
    return {
        key: value
        for key, value in data.items()
        if key in CREATE_TASK_FIELDS
    }


def update_task_schema(data):
    """Return only fields allowed during task updates."""
    return {
        key: value
        for key, value in data.items()
        if key in UPDATE_TASK_FIELDS
    }


def task_response_schema(data):
    """Return only fields exposed by the API response."""
    return {
        key: value
        for key, value in data.items()
        if key in RESPONSE_FIELDS
    }