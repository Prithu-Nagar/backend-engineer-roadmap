"""
LeetCode: 435. Non-overlapping Intervals

Pattern:
Intervals + Sorting + Greedy

Goal:
Remove the minimum number of intervals so that
the remaining intervals do not overlap.

Greedy idea:
When two intervals overlap, keep the interval that
ends earlier because it leaves more room for future intervals.

Time Complexity:
O(n log n)

Space Complexity:
O(1) apart from the sorting implementation.
"""


def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0

    intervals.sort(key=lambda interval: interval[1])

    removals = 0
    previous_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start < previous_end:
            removals += 1
        else:
            previous_end = end

    return removals


if __name__ == "__main__":
    examples = [
        [[1, 2], [2, 3], [3, 4], [1, 3]],
        [[1, 2], [1, 2], [1, 2]],
        [[1, 2], [2, 3]],
    ]

    for intervals in examples:
        print(f"Input:  {intervals}")
        print(f"Output: {erase_overlap_intervals(intervals)}")
        print()