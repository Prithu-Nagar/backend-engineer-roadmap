"""
LeetCode: Subsets

Day 20 — Recursion / Backtracking

Given an integer array containing unique elements, return all possible
subsets.

Approach:
For every element we have two choices:
1. Include it.
2. Exclude it.

This creates a recursion tree with 2^n possible subsets.
"""



def subsets(nums: list[int]) -> list[list[int]]:
    """Return all possible subsets of nums."""
    result: list[list[int]] = []
    current: list[int] = []

    def backtrack(index: int) -> None:
        if index == len(nums):
            result.append(current.copy())
            return

        # Include the current element.
        current.append(nums[index])
        backtrack(index + 1)

        # Undo the choice.
        current.pop()

        # Exclude the current element.
        backtrack(index + 1)

    backtrack(0)

    return result


if __name__ == "__main__":
    print(subsets([1, 2, 3]))