"""
LeetCode: Find Minimum in Rotated Sorted Array

Day 57 — Binary Search / Intervals

Find the minimum value in a rotated sorted array containing unique values.
"""

from __future__ import annotations


def find_min(nums: list[int]) -> int:
    """Return the minimum value using binary search."""
    if not nums:
        raise ValueError("nums must not be empty")

    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]


if __name__ == "__main__":
    print(find_min([4, 5, 6, 7, 0, 1, 2]))
