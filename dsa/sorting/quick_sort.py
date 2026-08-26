"""
Quick Sort

Pattern:
Divide and conquer / partitioning

Time Complexity:
- Best: O(N log N)
- Average: O(N log N)
- Worst: O(N^2)

Space Complexity:
O(N) worst-case recursion depth.
"""


def quick_sort(values: list[int]) -> list[int]:
    """Return a sorted copy using recursive quicksort partitioning."""

    if len(values) <= 1:
        return values.copy()

    pivot = values[-1]
    smaller = [value for value in values[:-1] if value <= pivot]
    greater = [value for value in values[:-1] if value > pivot]

    return quick_sort(smaller) + [pivot] + quick_sort(greater)


if __name__ == "__main__":
    numbers = [10, 7, 8, 9, 1, 5]
    print(quick_sort(numbers))
