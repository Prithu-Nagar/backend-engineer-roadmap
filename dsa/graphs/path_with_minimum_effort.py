"""
Problem:
Path With Minimum Effort

Pattern:
Weighted grid graph / Dijkstra / minimax path

Time Complexity:
O(M * N * log(M * N))

Space Complexity:
O(M * N)
"""

import heapq
from typing import List


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        rows = len(heights)
        cols = len(heights[0])

        efforts = [[float("inf")] * cols for _ in range(rows)]
        efforts[0][0] = 0

        min_heap: list[tuple[int, int, int]] = [(0, 0, 0)]
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        while min_heap:
            effort, row, col = heapq.heappop(min_heap)

            if (row, col) == (rows - 1, cols - 1):
                return effort

            if effort > efforts[row][col]:
                continue

            for row_delta, col_delta in directions:
                next_row = row + row_delta
                next_col = col + col_delta

                if not (0 <= next_row < rows and 0 <= next_col < cols):
                    continue

                edge_effort = abs(
                    heights[row][col] - heights[next_row][next_col]
                )
                new_effort = max(effort, edge_effort)

                if new_effort < efforts[next_row][next_col]:
                    efforts[next_row][next_col] = new_effort
                    heapq.heappush(
                        min_heap,
                        (new_effort, next_row, next_col),
                    )

        return 0
