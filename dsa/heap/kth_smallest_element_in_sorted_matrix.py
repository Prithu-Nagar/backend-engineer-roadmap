"""
LeetCode: Kth Smallest Element in a Sorted Matrix

Pattern:
Min-heap over the first element from each active row.

Time Complexity:
O(k log n), where n is the number of rows.

Space Complexity:
O(n)
"""

from __future__ import annotations

import heapq


class Solution:
    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:
        heap: list[tuple[int, int, int]] = []

        for row in range(min(k, len(matrix))):
            heapq.heappush(heap, (matrix[row][0], row, 0))

        value = 0

        for _ in range(k):
            value, row, col = heapq.heappop(heap)

            if col + 1 < len(matrix[row]):
                heapq.heappush(heap, (matrix[row][col + 1], row, col + 1))

        return value


if __name__ == "__main__":
    solution = Solution()
    print(
        solution.kthSmallest(
            [
                [1, 5, 9],
                [10, 11, 13],
                [12, 13, 15],
            ],
            8,
        )
    )
