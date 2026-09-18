"""
Day 49 — Maximum Subarray

Mixed timed-review problem: maintain the best subarray ending at the current
position and the best answer seen so far.
"""

from __future__ import annotations


def max_sub_array(nums: list[int]) -> int:
    """Return the maximum sum of any non-empty contiguous subarray."""

    if not nums:
        raise ValueError("nums must contain at least one value")

    current = best = nums[0]

    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)

    return best


if __name__ == "__main__":
    print(max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
