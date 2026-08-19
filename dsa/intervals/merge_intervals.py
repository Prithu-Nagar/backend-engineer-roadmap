"""
LeetCode: 56. Merge Intervals

Pattern:
Intervals + Sorting + Merging

Time Complexity:
O(n log n)

Space Complexity:
O(n) for the result.
"""


def merge(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    intervals.sort(key=lambda interval: interval[0])

    merged = [intervals[0]]

    for current_start, current_end in intervals[1:]:
        previous_end = merged[-1][1]

        if current_start <= previous_end:
            merged[-1][1] = max(previous_end, current_end)
        else:
            merged.append([current_start, current_end])

    return merged


if __name__ == "__main__":
    examples = [
        [[1, 3], [2, 6], [8, 10], [9, 12]],
        [[1, 4], [4, 5]],
        [[1, 2], [3, 4]],
    ]

    for intervals in examples:
        print(f"Input:  {intervals}")
        print(f"Output: {merge(intervals)}")
        print()