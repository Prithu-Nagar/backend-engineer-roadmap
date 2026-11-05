"""Database-backed Task Manager routes with authenticated ownership checks."""

from __future__ import annotations

from flask import Blueprint, g, jsonify, request
from sqlalchemy import func, select

if __package__:
    from .auth import login_required
    from .extensions import db
    from .models import Task
else:  # pragma: no cover - Docker runs modules as top-level imports
    from auth import login_required
    from extensions import db
    from models import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

ALLOWED_STATUSES = frozenset({"pending", "in_progress", "completed"})
ALLOWED_PRIORITIES = frozenset({"low", "medium", "high"})
WRITABLE_FIELDS = frozenset({"title", "description", "status", "priority"})
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def _error(code: str, message: str, status: int):
    """Build the API's standard error response."""
    return jsonify({"error": {"code": code, "message": message}}), status


def _task_payload(task: Task) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }


def _visible_task(task_id: int) -> Task | None:
    """Return a task only when it belongs to the caller (admins can inspect all)."""
    statement = select(Task).where(Task.id == task_id)
    if g.current_user.role != "admin":
        statement = statement.where(Task.user_id == g.current_user.id)
    return db.session.scalar(statement)


def _request_object() -> dict | None:
    """Return a JSON object, rejecting arrays, scalars and malformed JSON."""
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


def _validate_task_fields(data: dict, *, partial: bool = False) -> str | None:
    """Validate writable task fields and return a useful error message."""
    if not data:
        if partial:
            return "At least one task field is required."
        return "Task data is required."
    unsupported = set(data) - WRITABLE_FIELDS
    if unsupported:
        return f"Unsupported task fields: {', '.join(sorted(unsupported))}."

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            return "Title must be a non-empty string."
        if len(title.strip()) > 200:
            return "Title must contain at most 200 characters."

    if (
        "description" in data
        and data["description"] is not None
        and not isinstance(data["description"], str)
    ):
        return "Description must be a string or null."

    if "status" in data and (
        not isinstance(data["status"], str)
        or data["status"] not in ALLOWED_STATUSES
    ):
        return "Status must be pending, in_progress, or completed."

    if "priority" in data and (
        not isinstance(data["priority"], str)
        or data["priority"] not in ALLOWED_PRIORITIES
    ):
        return "Priority must be low, medium, or high."

    return None


def _parse_list_parameters():
    """Validate list filters and pagination; return (values, error)."""
    raw_page = request.args.get("page", "1")
    raw_per_page = request.args.get("per_page", str(DEFAULT_PAGE_SIZE))
    try:
        page = int(raw_page)
        per_page = int(raw_per_page)
    except (TypeError, ValueError):
        return None, "Page and per_page must be integers."
    if page < 1:
        return None, "Page must be at least 1."
    if not 1 <= per_page <= MAX_PAGE_SIZE:
        return None, f"per_page must be between 1 and {MAX_PAGE_SIZE}."

    status = request.args.get("status")
    priority = request.args.get("priority")
    if status is not None and status not in ALLOWED_STATUSES:
        return None, "Unsupported status filter."
    if priority is not None and priority not in ALLOWED_PRIORITIES:
        return None, "Unsupported priority filter."

    search = request.args.get("search", "").strip()
    if len(search) > 200:
        return None, "Search text must contain at most 200 characters."

    sort_by = request.args.get("sort_by", "created_at")
    sort_order = request.args.get("sort_order", "desc").lower()
    sort_columns = {
        "id": Task.id,
        "title": Task.title,
        "status": Task.status,
        "priority": Task.priority,
        "created_at": Task.created_at,
        "updated_at": Task.updated_at,
    }
    if sort_by not in sort_columns:
        return None, "Unsupported sort_by field."
    if sort_order not in {"asc", "desc"}:
        return None, "sort_order must be 'asc' or 'desc'."

    return {
        "page": page,
        "per_page": per_page,
        "status": status,
        "priority": priority,
        "search": search,
        "sort_column": sort_columns[sort_by],
        "sort_order": sort_order,
    }, None


@task_bp.get("/")
@login_required
def get_tasks():
    """List visible tasks with database-backed filters and pagination."""
    params, error = _parse_list_parameters()
    if error:
        return _error("VALIDATION_ERROR", error, 422)

    filters = []
    if g.current_user.role != "admin":
        filters.append(Task.user_id == g.current_user.id)
    if params["status"]:
        filters.append(Task.status == params["status"])
    if params["priority"]:
        filters.append(Task.priority == params["priority"])
    if params["search"]:
        filters.append(Task.title.ilike(f"%{params['search']}%"))

    total = db.session.scalar(
        select(func.count()).select_from(Task).where(*filters)
    ) or 0
    ordering = (
        params["sort_column"].asc()
        if params["sort_order"] == "asc"
        else params["sort_column"].desc()
    )
    statement = (
        select(Task)
        .where(*filters)
        .order_by(ordering, Task.id.desc())
        .offset((params["page"] - 1) * params["per_page"])
        .limit(params["per_page"])
    )
    tasks = db.session.scalars(statement).all()
    pages = (total + params["per_page"] - 1) // params["per_page"]

    return jsonify({
        "tasks": [_task_payload(task) for task in tasks],
        "pagination": {
            "page": params["page"],
            "per_page": params["per_page"],
            "total": total,
            "pages": pages,
            "has_next": params["page"] < pages,
            "has_previous": params["page"] > 1,
        },
    }), 200


@task_bp.get("/<int:task_id>")
@login_required
def get_task(task_id: int):
    """Retrieve one task without disclosing another user's resources."""
    task = _visible_task(task_id)
    if task is None:
        return _error("TASK_NOT_FOUND", "Task not found.", 404)
    return jsonify({"task": _task_payload(task)}), 200


@task_bp.post("/")
@login_required
def create_task():
    """Create a task owned by the authenticated user."""
    data = _request_object()
    if data is None:
        return _error("INVALID_REQUEST", "A JSON object is required.", 400)
    error = _validate_task_fields(data)
    if error:
        return _error("VALIDATION_ERROR", error, 422)

    try:
        task = Task(user_id=g.current_user.id, **data)
        db.session.add(task)
        db.session.commit()
    except (TypeError, ValueError) as exc:
        db.session.rollback()
        return _error("VALIDATION_ERROR", str(exc), 422)

    return jsonify({"task": _task_payload(task)}), 201


@task_bp.patch("/<int:task_id>")
@login_required
def update_task(task_id: int):
    """Partially update a visible task after validating the writable fields."""
    data = _request_object()
    if data is None:
        return _error("INVALID_REQUEST", "A JSON object is required.", 400)
    error = _validate_task_fields(data, partial=True)
    if error:
        return _error("VALIDATION_ERROR", error, 422)

    task = _visible_task(task_id)
    if task is None:
        return _error("TASK_NOT_FOUND", "Task not found.", 404)

    try:
        for field, value in data.items():
            setattr(task, field, value.strip() if field == "title" else value)
        db.session.commit()
    except (TypeError, ValueError) as exc:
        db.session.rollback()
        return _error("VALIDATION_ERROR", str(exc), 422)

    return jsonify({"task": _task_payload(task)}), 200


@task_bp.delete("/<int:task_id>")
@login_required
def delete_task(task_id: int):
    """Delete a visible task without disclosing foreign-owned resources."""
    task = _visible_task(task_id)
    if task is None:
        return _error("TASK_NOT_FOUND", "Task not found.", 404)
    db.session.delete(task)
    db.session.commit()
    return "", 204


@task_bp.get("/search")
@login_required
def search_tasks():
    """Preserve the original search URL while using the persisted task collection."""
    query = request.args.get("query", "").strip()
    if len(query) > 200:
        return _error(
            "VALIDATION_ERROR",
            "Search text must contain at most 200 characters.",
            422,
        )
    statement = select(Task).where(Task.title.ilike(f"%{query}%")).order_by(Task.id)
    if g.current_user.role != "admin":
        statement = statement.where(Task.user_id == g.current_user.id)
    tasks = db.session.scalars(statement).all()
    return jsonify({
        "query": query,
        "tasks": [_task_payload(task) for task in tasks],
    }), 200
