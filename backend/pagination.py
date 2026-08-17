"""
Day 17 - API Pagination

Demonstrates parsing pagination, filtering, and sorting query parameters
for a Flask API.
"""

from flask import Blueprint, jsonify, request


pagination_bp = Blueprint(
    "pagination",
    __name__,
    url_prefix="/api/paginated-tasks",
)


SAMPLE_TASKS = [
    {"id": 1, "title": "Learn Flask", "completed": False, "priority": 3},
    {"id": 2, "title": "Write tests", "completed": True, "priority": 4},
    {"id": 3, "title": "Study SQL", "completed": False, "priority": 2},
    {"id": 4, "title": "Practice DSA", "completed": False, "priority": 5},
    {"id": 5, "title": "Review Python", "completed": True, "priority": 3},
]


def parse_positive_int(value, default, maximum=None):
    """Parse a positive integer query parameter safely."""
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default

    if parsed < 1:
        return default

    if maximum is not None:
        return min(parsed, maximum)

    return parsed


def paginate_items(items, page=1, per_page=10):
    """Return one page plus pagination metadata."""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page

    return {
        "items": items[start:end],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "has_next": end < total,
            "has_previous": page > 1,
        },
    }


@pagination_bp.route("", methods=["GET"])
def get_paginated_tasks():
    """Return tasks with pagination, filtering, and sorting."""
    page = parse_positive_int(request.args.get("page"), 1)

    per_page = parse_positive_int(
        request.args.get("per_page"),
        10,
        maximum=100,
    )

    tasks = list(SAMPLE_TASKS)

    completed = request.args.get("completed")

    if completed in {"true", "false"}:
        completed_value = completed == "true"

        tasks = [
            task
            for task in tasks
            if task["completed"] == completed_value
        ]

    sort_by = request.args.get("sort_by", "id")
    sort_order = request.args.get("sort_order", "asc")

    allowed_sort_fields = {"id", "title", "priority"}

    if sort_by not in allowed_sort_fields:
        return jsonify({
            "error": "Invalid sort_by field"
        }), 400

    if sort_order not in {"asc", "desc"}:
        return jsonify({
            "error": "sort_order must be 'asc' or 'desc'"
        }), 400

    tasks.sort(
        key=lambda task: task[sort_by],
        reverse=sort_order == "desc",
    )

    result = paginate_items(tasks, page, per_page)

    return jsonify(result), 200


if __name__ == "__main__":
    print(paginate_items(SAMPLE_TASKS, page=1, per_page=2))