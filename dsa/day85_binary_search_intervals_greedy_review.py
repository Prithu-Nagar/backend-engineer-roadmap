"""Day 85 — Binary search, intervals, and greedy review."""


def lower_bound(nums: list[int], target: int) -> int:
    """Return the first index whose value is >= target, or len(nums)."""
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


def can_reach_end(jumps: list[int]) -> bool:
    """Greedily track the farthest reachable index."""
    if not jumps:
        return False
    farthest = 0
    for index, jump in enumerate(jumps):
        if index > farthest:
            return False
        if jump < 0:
            raise ValueError("jump lengths must be non-negative")
        farthest = max(farthest, index + jump)
        if farthest >= len(jumps) - 1:
            return True
    return True


def run_smoke_tests() -> None:
    assert lower_bound([1, 2, 2, 4], 2) == 1
    assert lower_bound([1, 3, 5], 4) == 2
    assert lower_bound([], 1) == 0
    assert merge_intervals([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]
    assert merge_intervals([]) == []
    assert can_reach_end([2, 3, 1, 1, 4]) is True
    assert can_reach_end([3, 2, 1, 0, 4]) is False


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 85 DSA review checks passed.")
