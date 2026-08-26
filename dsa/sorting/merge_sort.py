"""
Merge Sort

Pattern:
Divide and conquer / stable sorting

Time Complexity:
- Best: O(N log N)
- Average: O(N log N)
- Worst: O(N log N)

Space Complexity:
O(N)
"""


def merge_sort(values: list[int]) -> list[int]:
    """Return a sorted copy of the input using stable merge sort."""

    if len(values) <= 1:
        return values.copy()

    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])

    merged: list[int] = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


if __name__ == "__main__":
    numbers = [38, 27, 43, 3, 9, 82, 10]
    print(merge_sort(numbers))
