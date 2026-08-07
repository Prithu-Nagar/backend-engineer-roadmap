"""
Flask Routing and Blueprints

Demonstrates:
- Dynamic URL parameters
- Query parameters
- HTTP methods
- Flask Blueprints
"""

from flask import Blueprint, jsonify, request


# ---------------------------------------
# Task Blueprint
# ---------------------------------------

task_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/api/tasks"
)


# ---------------------------------------
# Get All Tasks
# ---------------------------------------

@task_bp.route("/", methods=["GET"])
def get_tasks():
    return jsonify({
        "tasks": []
    })


# ---------------------------------------
# Get Single Task
# ---------------------------------------

@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    return jsonify({
        "task_id": task_id
    })


# ---------------------------------------
# Create Task
# ---------------------------------------

@task_bp.route("/", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}

    return jsonify({
        "message": "Task created",
        "task": data
    }), 201


# ---------------------------------------
# Search Tasks
# ---------------------------------------

@task_bp.route("/search", methods=["GET"])
def search_tasks():
    query = request.args.get("query", "")

    return jsonify({
        "query": query,
        "tasks": []
    })