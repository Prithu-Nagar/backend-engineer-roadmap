"""
Flask Request and Response Handling

Demonstrates path parameters, query parameters,
JSON request bodies, validation, and HTTP status codes.
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    return {
        "task_id": task_id
    }, 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    completed = request.args.get("completed")

    return {
        "completed": completed
    }, 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not data or not data.get("title"):
        return {
            "error": "Title is required"
        }, 400

    return {
        "message": "Task created",
        "title": data["title"]
    }, 201


if __name__ == "__main__":
    app.run(debug=True)