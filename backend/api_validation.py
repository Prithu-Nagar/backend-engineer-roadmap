"""
Day 16 - API Validation

Topics:
- Required fields
- Type validation
- Length validation
- Allowed fields
- Input sanitization
"""


ALLOWED_CREATE_FIELDS = {
    "title",
    "description",
    "completed",
    "priority",
}

ALLOWED_UPDATE_FIELDS = ALLOWED_CREATE_FIELDS


def sanitize_string(value):
    """Normalize a string value."""
    if not isinstance(value, str):
        return value

    return value.strip()


def validate_task_payload(payload, partial=False):
    """
    Validate and sanitize a Task Manager payload.

    Returns:
        (validated_data, errors)
    """
    if not isinstance(payload, dict):
        return {}, {"body": "Request body must be a JSON object."}

    allowed_fields = (
        ALLOWED_UPDATE_FIELDS if partial else ALLOWED_CREATE_FIELDS
    )

    errors = {}
    validated = {}

    unexpected_fields = set(payload) - allowed_fields

    if unexpected_fields:
        errors["fields"] = (
            f"Unexpected fields: {sorted(unexpected_fields)}"
        )

    if not partial and "title" not in payload:
        errors["title"] = "Title is required."

    if "title" in payload:
        title = sanitize_string(payload["title"])

        if not isinstance(title, str):
            errors["title"] = "Title must be a string."
        elif not title:
            errors["title"] = "Title cannot be empty."
        elif len(title) > 200:
            errors["title"] = "Title must not exceed 200 characters."
        else:
            validated["title"] = title

    if "description" in payload:
        description = sanitize_string(payload["description"])

        if not isinstance(description, str):
            errors["description"] = "Description must be a string."
        elif len(description) > 2000:
            errors["description"] = (
                "Description must not exceed 2000 characters."
            )
        else:
            validated["description"] = description

    if "completed" in payload:
        completed = payload["completed"]

        if not isinstance(completed, bool):
            errors["completed"] = "Completed must be a boolean."
        else:
            validated["completed"] = completed

    if "priority" in payload:
        priority = payload["priority"]

        if not isinstance(priority, int) or isinstance(priority, bool):
            errors["priority"] = "Priority must be an integer."
        elif not 1 <= priority <= 5:
            errors["priority"] = "Priority must be between 1 and 5."
        else:
            validated["priority"] = priority

    return validated, errors


if __name__ == "__main__":
    valid_payload = {
        "title": "   Learn Python   ",
        "description": "Backend engineering",
        "completed": False,
        "priority": 3,
    }

    invalid_payload = {
        "title": "",
        "completed": "yes",
        "priority": 10,
        "is_admin": True,
    }

    print("Valid payload:")
    print(validate_task_payload(valid_payload))

    print("\nInvalid payload:")
    print(validate_task_payload(invalid_payload))