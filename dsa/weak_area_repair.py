"""
Day 80 — DSA weak-area repair.

A small, testable repair set for common interview fundamentals. Use the
weakest pattern identified in Day 79 first, then run the smoke tests.
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """Return indices of two values summing to target, or raise ValueError.

    Time: O(n). Space: O(n).
    """
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    raise ValueError("no pair sums to target")


def lower_bound(nums: list[int], target: int) -> int:
    """Return the first index with value >= target, or len(nums).

    Requires nums to be sorted in non-decreasing order.
    Time: O(log n). Space: O(1).
    """
    left, right = 0, len(nums)
    while left < right:
        middle = left + (right - left) // 2
        if nums[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping closed intervals without mutating the input."""
    merged: list[list[int]] = []
    for start, end in sorted((item[0], item[1]) for item in intervals):
        if start > end:
            raise ValueError("interval start must not exceed end")
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def run_smoke_tests() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert lower_bound([1, 2, 2, 2, 5], 2) == 1
    assert lower_bound([1, 3, 5], 4) == 2
    assert lower_bound([], 10) == 0
    assert merge_intervals([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]
    try:
        two_sum([1, 2], 9)
    except ValueError:
        pass
    else:
        raise AssertionError("missing pair must raise ValueError")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 80 DSA weak-area repair passed.")
