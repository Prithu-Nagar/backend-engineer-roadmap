"""
LeetCode: Search a 2D Matrix II

Day 57 — Binary Search / Intervals

Search a matrix where every row is sorted left-to-right and every column is
sorted top-to-bottom.
"""

from __future__ import annotations


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """Return True when target exists in the sorted matrix."""
    if not matrix or not matrix[0]:
        return False

    row = 0
    col = len(matrix[0]) - 1

    while row < len(matrix) and col >= 0:
        value = matrix[row][col]

        if value == target:
            return True
        if value > target:
            col -= 1
        else:
            row += 1

    return False


if __name__ == "__main__":
    matrix = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]

    print(search_matrix(matrix, 5))
    print(search_matrix(matrix, 20))
