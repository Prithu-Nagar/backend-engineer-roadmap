from dataclasses import dataclass
from typing import Any

from flask import Flask, jsonify


app = Flask(__name__)


@dataclass
class APIError:
    status_code: int
    code: str
    message: str
    details: Any = None

    def to_response(self):
        body = {
            "error": {
                "code": self.code,
                "message": self.message,
            }
        }

        if self.details is not None:
            body["error"]["details"] = self.details

        return jsonify(body), self.status_code


BAD_REQUEST = APIError(
    status_code=400,
    code="BAD_REQUEST",
    message="The request is invalid.",
)

UNAUTHORIZED = APIError(
    status_code=401,
    code="UNAUTHORIZED",
    message="Authentication is required.",
)

FORBIDDEN = APIError(
    status_code=403,
    code="FORBIDDEN",
    message="You do not have permission to perform this action.",
)

NOT_FOUND = APIError(
    status_code=404,
    code="NOT_FOUND",
    message="The requested resource was not found.",
)

CONFLICT = APIError(
    status_code=409,
    code="CONFLICT",
    message="The request conflicts with the current resource state.",
)

INTERNAL_SERVER_ERROR = APIError(
    status_code=500,
    code="INTERNAL_SERVER_ERROR",
    message="An unexpected error occurred.",
)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    if task_id <= 0:
        return BAD_REQUEST.to_response()

    if task_id != 1:
        return APIError(
            status_code=404,
            code="TASK_NOT_FOUND",
            message="The requested task was not found.",
        ).to_response()

    return jsonify(
        {
            "id": 1,
            "title": "Learn Flask",
            "completed": False,
        }
    ), 200


@app.errorhandler(404)
def handle_not_found(error):
    return NOT_FOUND.to_response()


@app.errorhandler(500)
def handle_internal_error(error):
    return INTERNAL_SERVER_ERROR.to_response()


if __name__ == "__main__":
    app.run(debug=True)