"""
LeetCode: Combination Sum

Day 20 — Recursion / Backtracking

Given an array of distinct integers and a target, return all unique
combinations whose values sum to the target.

A candidate may be selected multiple times.

Approach:
Use backtracking with a start index.

The same index is passed into the recursive call because the current
candidate can be reused.
"""

from typing import List


def combination_sum(
    candidates: List[int],
    target: int,
) -> List[List[int]]:
    """Return all combinations whose sum equals target."""
    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(current.copy())
            return

        if remaining < 0:
            return

        for index in range(start, len(candidates)):
            candidate = candidates[index]

            if candidate > remaining:
                continue

            current.append(candidate)

            # Use the same index because a candidate can be reused.
            backtrack(index, remaining - candidate)

            current.pop()

    backtrack(0, target)

    return result


if __name__ == "__main__":
    print(combination_sum([2, 3, 6, 7], 7))