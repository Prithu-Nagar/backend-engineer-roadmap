"""
Day 78 — Build-a-REST-API timed exercise.

A compact Flask Task API with validation, consistent error responses,
deterministic pagination, and in-memory storage. The storage is intentionally
ephemeral; replace it with a repository/database for production use.
"""

from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)
    tasks: dict[int, dict[str, object]] = {}
    next_id = 1
    allowed_statuses = {"pending", "in_progress", "completed"}

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(error={"code": "not_found", "message": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify(error={"code": "method_not_allowed", "message": "Method not allowed"}), 405

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    @app.post("/api/v1/tasks")
    def create_task():
        nonlocal next_id
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error={"code": "invalid_json", "message": "Expected a JSON object"}), 400

        title = payload.get("title")
        if not isinstance(title, str) or not title.strip():
            return jsonify(error={"code": "validation_error", "message": "title must be non-empty"}), 400
        if len(title.strip()) > 200:
            return jsonify(error={"code": "validation_error", "message": "title must be at most 200 characters"}), 400

        task = {"id": next_id, "title": title.strip(), "status": "pending"}
        tasks[next_id] = task
        next_id += 1
        return jsonify(data=task), 201

    @app.get("/api/v1/tasks")
    def list_tasks():
        try:
            limit = int(request.args.get("limit", "20"))
            offset = int(request.args.get("offset", "0"))
        except ValueError:
            return jsonify(error={"code": "validation_error", "message": "limit and offset must be integers"}), 400
        if not 1 <= limit <= 100 or offset < 0:
            return jsonify(error={"code": "validation_error", "message": "limit must be 1..100 and offset non-negative"}), 400

        ordered = sorted(tasks.values(), key=lambda item: int(item["id"]))
        page = ordered[offset : offset + limit]
        return jsonify(data=page, pagination={"limit": limit, "offset": offset, "count": len(page)}), 200

    @app.get("/api/v1/tasks/<int:task_id>")
    def get_task(task_id: int):
        task = tasks.get(task_id)
        if task is None:
            return jsonify(error={"code": "not_found", "message": "Task not found"}), 404
        return jsonify(data=task), 200

    @app.patch("/api/v1/tasks/<int:task_id>")
    def update_task(task_id: int):
        task = tasks.get(task_id)
        if task is None:
            return jsonify(error={"code": "not_found", "message": "Task not found"}), 404
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error={"code": "invalid_json", "message": "Expected a JSON object"}), 400

        if "title" in payload:
            title = payload["title"]
            if not isinstance(title, str) or not title.strip() or len(title.strip()) > 200:
                return jsonify(error={"code": "validation_error", "message": "title must be non-empty and at most 200 characters"}), 400
            task["title"] = title.strip()
        if "status" in payload:
            status = payload["status"]
            if status not in allowed_statuses:
                return jsonify(error={"code": "validation_error", "message": "Invalid task status"}), 400
            task["status"] = status
        if not ({"title", "status"} & payload.keys()):
            return jsonify(error={"code": "validation_error", "message": "Provide title and/or status"}), 400
        return jsonify(data=task), 200

    @app.delete("/api/v1/tasks/<int:task_id>")
    def delete_task(task_id: int):
        if tasks.pop(task_id, None) is None:
            return jsonify(error={"code": "not_found", "message": "Task not found"}), 404
        return "", 204

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=False)
