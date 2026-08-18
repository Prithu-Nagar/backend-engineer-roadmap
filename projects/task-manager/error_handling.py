"""
Day 18 - Task Manager Error Handling

Provides consistent application-level error responses for the
Task Manager project.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class TaskManagerError:
    code: str
    message: str
    status_code: int
    details: Any = None

    def to_response(self):
        response = {
            "error": {
                "code": self.code,
                "message": self.message,
            }
        }

        if self.details is not None:
            response["error"]["details"] = self.details

        return response, self.status_code


BAD_REQUEST = TaskManagerError(
    code="BAD_REQUEST",
    message="The request is invalid.",
    status_code=400,
)

UNAUTHORIZED = TaskManagerError(
    code="UNAUTHORIZED",
    message="Authentication is required.",
    status_code=401,
)

FORBIDDEN = TaskManagerError(
    code="FORBIDDEN",
    message="You do not have permission to perform this action.",
    status_code=403,
)

NOT_FOUND = TaskManagerError(
    code="NOT_FOUND",
    message="The requested resource was not found.",
    status_code=404,
)

CONFLICT = TaskManagerError(
    code="CONFLICT",
    message="The request conflicts with the current resource state.",
    status_code=409,
)

TASK_NOT_FOUND = TaskManagerError(
    code="TASK_NOT_FOUND",
    message="The requested task was not found.",
    status_code=404,
)

INVALID_TASK = TaskManagerError(
    code="INVALID_TASK",
    message="The task data is invalid.",
    status_code=400,
)