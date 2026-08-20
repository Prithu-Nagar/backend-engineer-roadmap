"""
LeetCode: Permutations

Day 20 — Recursion / Backtracking

Given an array of distinct integers, return all possible permutations.

Approach:
At every recursion level, choose one unused element and add it to the
current permutation.

After the recursive call completes, undo the choice.
"""

from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    """Return all possible permutations of nums."""
    result: List[List[int]] = []
    current: List[int] = []
    used = [False] * len(nums)

    def backtrack() -> None:
        if len(current) == len(nums):
            result.append(current.copy())
            return

        for index, value in enumerate(nums):
            if used[index]:
                continue

            used[index] = True
            current.append(value)

            backtrack()

            current.pop()
            used[index] = False

    backtrack()

    return result


if __name__ == "__main__":
    print(permute([1, 2, 3]))