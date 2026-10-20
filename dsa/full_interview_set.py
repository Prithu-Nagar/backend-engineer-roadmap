"""Day 81 — Full interview set: arrays, hashing, intervals, and graphs."""
from collections import deque


def two_sum(nums: list[int], target: int) -> list[int]:
    """Return the first matching pair of indices in one pass. O(n) time/space."""
    seen: dict[int, int] = {}
    for i, value in enumerate(nums):
        if target - value in seen:
            return [seen[target - value], i]
        seen[value] = i
    raise ValueError("no pair sums to target")


def lower_bound(nums: list[int], target: int) -> int:
    """Return the first index whose value is >= target. O(log n) time, O(1) space."""
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping closed intervals. O(n log n) time, O(n) output space."""
    ordered = sorted((start, end) for start, end in intervals)
    merged: list[list[int]] = []
    for start, end in ordered:
        if start > end:
            raise ValueError("interval start must not exceed end")
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def shortest_path_length(graph: dict[int, list[int]], start: int, target: int) -> int:
    """Return unweighted shortest-path edge count, or -1 when unreachable. O(V+E)."""
    if start == target:
        return 0
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        node, distance = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor == target:
                return distance + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    return -1


def run_smoke_tests() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert lower_bound([1, 2, 2, 4], 2) == 1
    assert lower_bound([1, 3, 5], 6) == 3
    assert merge_intervals([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]
    assert shortest_path_length({1: [2, 3], 2: [4], 3: [4]}, 1, 4) == 2
    assert shortest_path_length({1: [2], 2: []}, 1, 9) == -1
    try:
        two_sum([1, 2], 10)
    except ValueError:
        pass
    else:
        raise AssertionError("missing pair must raise ValueError")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 81 DSA interview set passed.")
