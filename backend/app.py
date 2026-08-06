"""
Task Manager API

This file contains the primary Flask application developed throughout the
Backend Engineer Roadmap.

The application is extended incrementally as new backend concepts are learned,
making it a single evolving project rather than multiple isolated examples.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {
        "id": 1,
        "title": "Learn Flask",
        "completed": False
    },
    {
        "id": 2,
        "title": "Build REST API",
        "completed": False
    }
]


@app.route("/")
def home():
    return jsonify({"message": "Task Manager REST API"})


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


# Get a single task
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


# Create a task
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": data.get("completed", False)
    }

    tasks.append(new_task)

    return jsonify(new_task), 201


# Update a task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()

    task["title"] = data.get("title", task["title"])
    task["completed"] = data.get("completed", task["completed"])

    return jsonify(task), 200


# Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task)

    return jsonify({"message": "Task deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)