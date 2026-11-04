"""Database-backed Task Manager routes with authenticated ownership checks."""

from __future__ import annotations

from flask import Blueprint, g, jsonify, request
from sqlalchemy import select

if __package__:
    from .auth import login_required
    from .extensions import db
    from .models import Task
else:  # pragma: no cover - Docker runs modules as top-level imports
    from auth import login_required
    from extensions import db
    from models import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


def _task_payload(task: Task) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }


def _visible_task(task_id: int) -> Task | None:
    """Return a task only when it belongs to the caller (admins can inspect all)."""
    statement = select(Task).where(Task.id == task_id)
    if g.current_user.role != "admin":
        statement = statement.where(Task.user_id == g.current_user.id)
    return db.session.scalar(statement)


@task_bp.get("/")
@login_required
def get_tasks():
    """List only the authenticated user's tasks; admins can list all tasks."""
    statement = select(Task).order_by(Task.id)
    if g.current_user.role != "admin":
        statement = statement.where(Task.user_id == g.current_user.id)
    tasks = db.session.scalars(statement).all()
    return jsonify({"tasks": [_task_payload(task) for task in tasks]}), 200


@task_bp.get("/<int:task_id>")
@login_required
def get_task(task_id: int):
    task = _visible_task(task_id)
    if task is None:
        # Return 404 for both absent and foreign-owned resources to avoid
        # disclosing whether another user's task exists.
        return jsonify({"error": {"code": "TASK_NOT_FOUND", "message": "Task not found."}}), 404
    return jsonify({"task": _task_payload(task)}), 200


@task_bp.post("/")
@login_required
def create_task():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": "A JSON object is required."}}), 400
    allowed = {"title", "description", "status", "priority"}
    if set(data) - allowed:
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": "Unsupported task fields were supplied."}}), 400
    title = data.get("title")
    description = data.get("description")
    status = data.get("status", "pending")
    priority = data.get("priority", "medium")
    if not isinstance(title, str) or not title.strip() or len(title.strip()) > 200:
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": "Title must contain 1 to 200 characters."}}), 400
    if description is not None and not isinstance(description, str):
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": "Description must be a string."}}), 400
    if status not in {"pending", "in_progress", "completed"}:
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": "Unsupported task status."}}), 400
    if priority not in {"low", "medium", "high"}:
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": "Unsupported task priority."}}), 400

    try:
        task = Task(
            user_id=g.current_user.id,
            title=title,
            description=description,
            status=status,
            priority=priority,
        )
        db.session.add(task)
        db.session.commit()
    except (TypeError, ValueError) as exc:
        db.session.rollback()
        return jsonify({"error": {"code": "INVALID_REQUEST", "message": str(exc)}}), 400

    return jsonify({"task": _task_payload(task)}), 201


@task_bp.get("/search")
@login_required
def search_tasks():
    query = request.args.get("query", "")
    statement = select(Task).where(Task.title.ilike(f"%{query}%")).order_by(Task.id)
    if g.current_user.role != "admin":
        statement = statement.where(Task.user_id == g.current_user.id)
    tasks = db.session.scalars(statement).all()
    return jsonify({"query": query, "tasks": [_task_payload(task) for task in tasks]}), 200
