"""
LeetCode 992 - Subarrays with K Different Integers
Pattern: Sliding Window + Frequency Map
"""

from collections import defaultdict


def _at_most(nums: list[int], k: int) -> int:
    """Count subarrays containing at most k distinct values."""
    if k < 0:
        return 0

    counts = defaultdict(int)
    left = 0
    result = 0

    for right, value in enumerate(nums):
        if counts[value] == 0:
            k -= 1
        counts[value] += 1

        while k < 0:
            outgoing = nums[left]
            counts[outgoing] -= 1
            if counts[outgoing] == 0:
                k += 1
            left += 1

        result += right - left + 1

    return result


def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
    """Count subarrays containing exactly k distinct values."""
    return _at_most(nums, k) - _at_most(nums, k - 1)


if __name__ == "__main__":
    print(subarrays_with_k_distinct([1, 2, 1, 2, 3], 2))
