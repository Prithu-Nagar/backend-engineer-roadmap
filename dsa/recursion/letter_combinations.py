"""
Day 21 — Letter Combinations of a Phone Number

Backtracking pattern:
- Choose one letter for the current digit.
- Recurse to the next digit.
- Remove the chosen letter when returning.

LeetCode: Letter Combinations of a Phone Number
"""

from typing import List


PHONE = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def letter_combinations(digits: str) -> List[str]:
    """Return every possible letter combination for the input digits."""

    if not digits:
        return []

    result: List[str] = []
    path: List[str] = []

    def backtrack(index: int) -> None:
        if index == len(digits):
            result.append("".join(path))
            return

        for letter in PHONE[digits[index]]:
            path.append(letter)
            backtrack(index + 1)
            path.pop()  # Restore state before exploring the next choice.

    backtrack(0)
    return result


if __name__ == "__main__":
    print(letter_combinations("23"))
