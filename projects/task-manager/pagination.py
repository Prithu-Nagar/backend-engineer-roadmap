"""
Day 17 - Task Manager Pagination, Filtering and Sorting

Application-level reference implementation used to demonstrate the API
pagination concepts before integrating them with a database-backed query.
"""

from typing import Iterable


ALLOWED_SORT_FIELDS = {"id", "title", "priority", "completed"}


def parse_pagination(page: str | None, per_page: str | None) -> tuple[int, int]:
    """Parse page and page-size values with safe defaults and limits."""
    try:
        parsed_page = int(page) if page is not None else 1
    except ValueError:
        parsed_page = 1

    try:
        parsed_per_page = int(per_page) if per_page is not None else 10
    except ValueError:
        parsed_per_page = 10

    parsed_page = max(parsed_page, 1)
    parsed_per_page = min(max(parsed_per_page, 1), 100)

    return parsed_page, parsed_per_page


def filter_tasks(
    tasks: Iterable[dict],
    completed: bool | None = None,
) -> list[dict]:
    """Filter tasks by completion state when supplied."""
    result = list(tasks)

    if completed is None:
        return result

    return [
        task
        for task in result
        if task.get("completed") == completed
    ]


def sort_tasks(
    tasks: Iterable[dict],
    sort_by: str = "id",
    sort_order: str = "asc",
) -> tuple[list[dict] | None, str | None]:
    """Sort tasks using an allow-listed field."""
    if sort_by not in ALLOWED_SORT_FIELDS:
        return None, f"Unsupported sort field: {sort_by}"

    if sort_order not in {"asc", "desc"}:
        return None, "sort_order must be 'asc' or 'desc'"

    result = sorted(
        tasks,
        key=lambda task: task.get(sort_by),
        reverse=sort_order == "desc",
    )

    return result, None


def paginate_tasks(
    tasks: Iterable[dict],
    page: str | None = None,
    per_page: str | None = None,
    completed: bool | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
) -> dict:
    """Apply filtering, sorting and pagination in the expected order."""
    current_page, page_size = parse_pagination(page, per_page)

    filtered = filter_tasks(tasks, completed)
    sorted_tasks, error = sort_tasks(
        filtered,
        sort_by,
        sort_order,
    )

    if error:
        return {"error": error}

    total = len(sorted_tasks)
    start = (current_page - 1) * page_size
    end = start + page_size

    return {
        "tasks": sorted_tasks[start:end],
        "pagination": {
            "page": current_page,
            "per_page": page_size,
            "total": total,
            "pages": (total + page_size - 1) // page_size,
            "has_next": end < total,
            "has_previous": current_page > 1,
        },
    }


if __name__ == "__main__":
    sample_tasks = [
        {
            "id": 1,
            "title": "Learn Flask",
            "completed": False,
            "priority": 3,
        },
        {
            "id": 2,
            "title": "Write tests",
            "completed": True,
            "priority": 4,
        },
        {
            "id": 3,
            "title": "Study SQL",
            "completed": False,
            "priority": 2,
        },
        {
            "id": 4,
            "title": "Practice DSA",
            "completed": False,
            "priority": 5,
        },
    ]

    print(
        paginate_tasks(
            sample_tasks,
            page="1",
            per_page="2",
            completed=False,
            sort_by="priority",
            sort_order="desc",
        )
    )