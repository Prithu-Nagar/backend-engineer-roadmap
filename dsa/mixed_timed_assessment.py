"""
Day 79 — Mixed DSA timed assessment.

Run this file directly to check representative array, graph, and interval
problems. Suggested assessment time: 45 minutes without notes.
"""

from collections import deque


def max_subarray(nums: list[int]) -> int:
    """Return the maximum sum of a non-empty contiguous subarray.

    Time: O(n). Space: O(1).
    """
    if not nums:
        raise ValueError("nums must not be empty")

    current = best = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best


def rotting_oranges(grid: list[list[int]]) -> int:
    """Return minutes for all reachable fresh oranges to rot, or -1.

    Time: O(rows * columns). Space: O(rows * columns).
    """
    if not grid or not grid[0]:
        return 0

    rows, columns = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for row in range(rows):
        for column in range(columns):
            if grid[row][column] == 2:
                queue.append((row, column, 0))
            elif grid[row][column] == 1:
                fresh += 1

    minutes = 0
    while queue:
        row, column, elapsed = queue.popleft()
        minutes = max(minutes, elapsed)
        for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_delta
            next_column = column + column_delta
            if (
                0 <= next_row < rows
                and 0 <= next_column < columns
                and grid[next_row][next_column] == 1
            ):
                grid[next_row][next_column] = 2
                fresh -= 1
                queue.append((next_row, next_column, elapsed + 1))

    return minutes if fresh == 0 else -1


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping intervals. Time: O(n log n), space: O(n)."""
    merged: list[list[int]] = []
    for start, end in sorted(intervals):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def run_smoke_tests() -> None:
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray([-3, -1, -2]) == -1
    assert rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert rotting_oranges([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6], [8, 10], [15, 18]
    ]


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 79 mixed DSA smoke tests passed.")
