"""
Task Manager - Day 16 Validation

Reusable validation helpers for the Task Manager API.
"""


def validate_required(value, field_name):
    """Validate a required value."""
    if value is None:
        return f"{field_name} is required."

    return None


def validate_string(
    value,
    field_name,
    required=False,
    min_length=0,
    max_length=None,
):
    """Validate a string field."""
    if value is None:
        return f"{field_name} is required." if required else None

    if not isinstance(value, str):
        return f"{field_name} must be a string."

    value = value.strip()

    if required and not value:
        return f"{field_name} cannot be empty."

    if len(value) < min_length:
        return f"{field_name} is too short."

    if max_length is not None and len(value) > max_length:
        return f"{field_name} is too long."

    return None


def validate_boolean(value, field_name):
    """Validate a boolean field."""
    if value is None:
        return None

    if not isinstance(value, bool):
        return f"{field_name} must be a boolean."

    return None


def validate_priority(value):
    """Validate task priority."""
    if value is None:
        return None

    if not isinstance(value, int) or isinstance(value, bool):
        return "priority must be an integer."

    if not 1 <= value <= 5:
        return "priority must be between 1 and 5."

    return None