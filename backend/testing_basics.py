"""
Testing Basics

Day 14 focus:
- Unit tests
- Test structure
- Assertions
- Pytest basics
- Fixtures
- Testing backend logic
"""

from __future__ import annotations


def add_numbers(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def is_even(value: int) -> bool:
    """Return whether a value is even."""
    return value % 2 == 0


def validate_username(username: str) -> bool:
    """Return whether a username is valid."""
    return bool(username and len(username) >= 3)


# Example pytest tests:
#
# def test_add_numbers():
#     assert add_numbers(2, 3) == 5
#
#
# def test_is_even():
#     assert is_even(8) is True
#     assert is_even(7) is False
#
#
# def test_validate_username():
#     assert validate_username("alice") is True
#     assert validate_username("ab") is False
#
#
# Example pytest fixture:
#
# @pytest.fixture
# def sample_user():
#     return {
#         "user_id": 1,
#         "username": "alice",
#         "role": "user",
#     }
#
#
# def test_user(sample_user):
#     assert sample_user["role"] == "user"


if __name__ == "__main__":
    assert add_numbers(2, 3) == 5
    assert is_even(8) is True
    assert is_even(7) is False
    assert validate_username("alice") is True
    print("Basic tests passed")