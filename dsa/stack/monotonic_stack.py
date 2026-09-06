"""
Monotonic Stack

A monotonic stack keeps values or indexes ordered while scanning a sequence.
It is useful for next-greater, next-smaller, and range-boundary problems.

Time Complexity:
O(N) for a single pass when each item is pushed and popped at most once.

Space Complexity:
O(N)
"""

from typing import Sequence


def next_greater_indices(values: Sequence[int]) -> list[int]:
    """Return the index of the next greater value for each position.

    A decreasing stack of indexes is maintained. When the current value is
    greater than the value at the stack top, the current index resolves that
    pending next-greater relationship.
    """
    result = [-1] * len(values)
    stack: list[int] = []

    for index, value in enumerate(values):
        while stack and values[stack[-1]] < value:
            result[stack.pop()] = index
        stack.append(index)

    return result


if __name__ == "__main__":
    sample = [2, 1, 2, 4, 3]
    print(next_greater_indices(sample))
