"""
Type Hints

Day 14 focus:
- Function annotations
- Optional values
- Union types
- Generic collections
- Type hints for API inputs and outputs
"""

from typing import Optional, Union


def greet(name: str) -> str:
    """Return a greeting for a user name."""
    return f"Hello, {name}!"


def parse_age(value: str) -> Optional[int]:
    """Convert an age string into an integer when possible."""
    try:
        return int(value)
    except ValueError:
        return None


def normalize_id(value: Union[int, str]) -> str:
    """Accept an integer or string ID and return it as a string."""
    return str(value)


def add_items(values: list[int]) -> int:
    """Sum a list of integers."""
    return sum(values)


def build_user_payload(
    user_id: int,
    name: str,
    tags: list[str],
) -> dict[str, Union[int, str, list[str]]]:
    """Build a typed API-style user payload."""
    return {
        "user_id": user_id,
        "name": name,
        "tags": tags,
    }


if __name__ == "__main__":
    print(greet("Backend Engineer"))
    print(parse_age("25"))
    print(parse_age("invalid"))
    print(normalize_id(101))
    print(normalize_id("user-101"))
    print(add_items([1, 2, 3, 4]))
    print(build_user_payload(1, "Alice", ["backend", "python"]))