"""
Task Manager API Routing

Demonstrates:
- Flask Blueprints
- Path parameters
- Query parameters
- JSON request bodies
- Basic request validation
- HTTP status codes
"""

from flask import Blueprint, jsonify, request


task_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/api/tasks",
)


@task_bp.route("/", methods=["GET"])
def get_tasks():
    completed = request.args.get("completed")

    response = {
        "tasks": []
    }

    if completed is not None:
        response["completed"] = completed

    return jsonify(response), 200


@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    return jsonify({
        "task_id": task_id
    }), 200


@task_bp.route("/", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not data or not data.get("title"):
        return jsonify({
            "error": "Title is required"
        }), 400

    return jsonify({
        "message": "Task created",
        "task": data
    }), 201


@task_bp.route("/search", methods=["GET"])
def search_tasks():
    query = request.args.get("query", "")

    return jsonify({
        "query": query,
        "tasks": []
    }), 200
