"""
Day 51 — Search a 2D Matrix

Treat a row-wise sorted matrix as one conceptual sorted array and use binary
search over its virtual indices.
"""


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """Return whether target exists in the sorted matrix.

    Time: O(log(m * n))
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False

    rows = len(matrix)
    cols = len(matrix[0])
    left, right = 0, rows * cols - 1

    while left <= right:
        middle = (left + right) // 2
        row, col = divmod(middle, cols)
        value = matrix[row][col]

        if value == target:
            return True
        if value < target:
            left = middle + 1
        else:
            right = middle - 1

    return False


if __name__ == "__main__":
    sample = [[1, 3, 5], [7, 9, 11], [13, 15, 17]]
    print(search_matrix(sample, 9))
