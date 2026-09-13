"""
LeetCode: 986. Interval List Intersections

Pattern:
Intervals + Two Pointers

Time Complexity:
O(n + m)

Space Complexity:
O(n + m) for the result.
"""


def interval_intersection(
    first_list: list[list[int]], second_list: list[list[int]]
) -> list[list[int]]:
    i = j = 0
    result = []

    while i < len(first_list) and j < len(second_list):
        start = max(first_list[i][0], second_list[j][0])
        end = min(first_list[i][1], second_list[j][1])

        if start <= end:
            result.append([start, end])

        if first_list[i][1] < second_list[j][1]:
            i += 1
        else:
            j += 1

    return result


if __name__ == "__main__":
    examples = [
        (
            [[0, 2], [5, 10], [13, 23], [24, 25]],
            [[1, 5], [8, 12], [15, 24], [25, 26]],
        ),
        ([[1, 3], [5, 9]], []),
    ]

    for first_list, second_list in examples:
        print(f"Input:  {first_list} and {second_list}")
        print(f"Output: {interval_intersection(first_list, second_list)}")
        print()
