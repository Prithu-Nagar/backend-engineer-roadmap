"""
Task Manager - Day 16 Schemas
Task Manager - Phase 2 Day 2 API Contract Schemas

Defines the canonical fields accepted by the Task Manager MVP API
for task creation, updates, and responses.
"""


CREATE_TASK_FIELDS = {
    "title",
    "description",
    "status",
    "priority",
}

UPDATE_TASK_FIELDS = CREATE_TASK_FIELDS

RESPONSE_FIELDS = {
    "id",
    "title",
    "description",
    "status",
    "priority",
    "created_at",
    "updated_at",
}

TASK_STATUSES = frozenset({"pending", "in_progress", "completed"})
TASK_PRIORITIES = frozenset({"low", "medium", "high"})
TASK_TITLE_MAX_LENGTH = 200
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


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