"""
LeetCode: 57. Insert Interval

Pattern:
Intervals + Sorting + Merging

Time Complexity:
O(n)

Space Complexity:
O(n) for the result.
"""


def insert(
    intervals: list[list[int]],
    new_interval: list[int],
) -> list[list[int]]:
    result = []

    index = 0
    interval_count = len(intervals)

    # Add intervals that completely end before the new interval.
    while (
        index < interval_count
        and intervals[index][1] < new_interval[0]
    ):
        result.append(intervals[index])
        index += 1

    # Merge overlapping intervals.
    while (
        index < interval_count
        and intervals[index][0] <= new_interval[1]
    ):
        new_interval[0] = min(
            new_interval[0],
            intervals[index][0],
        )
        new_interval[1] = max(
            new_interval[1],
            intervals[index][1],
        )
        index += 1

    result.append(new_interval)

    # Add remaining intervals.
    while index < interval_count:
        result.append(intervals[index])
        index += 1

    return result


if __name__ == "__main__":
    examples = [
        (
            [[1, 3], [6, 9]],
            [2, 5],
        ),
        (
            [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]],
            [4, 8],
        ),
        (
            [],
            [5, 7],
        ),
    ]

    for intervals, new_interval in examples:
        print(f"Intervals:    {intervals}")
        print(f"New interval: {new_interval}")
        print(f"Result:       {insert(intervals, new_interval)}")
        print()