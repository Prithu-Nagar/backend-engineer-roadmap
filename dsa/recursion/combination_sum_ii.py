"""
LeetCode: Combination Sum II

Day 47 — Backtracking review

Find unique combinations that sum to the target. Each candidate can be used
at most once, and duplicate values at the same recursion depth are skipped.
"""

from typing import List


def combination_sum2(candidates: List[int], target: int) -> List[List[int]]:
    """Return unique combinations whose values sum to target."""
    candidates.sort()
    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(current.copy())
            return

        for index in range(start, len(candidates)):
            value = candidates[index]

            if index > start and value == candidates[index - 1]:
                continue
            if value > remaining:
                break

            current.append(value)
            backtrack(index + 1, remaining - value)
            current.pop()

    backtrack(0, target)
    return result


if __name__ == "__main__":
    print(combination_sum2([10, 1, 2, 7, 6, 1, 5], 8))
