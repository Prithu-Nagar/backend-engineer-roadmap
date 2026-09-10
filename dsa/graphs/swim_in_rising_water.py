"""
Problem:
Swim in Rising Water

Pattern:
Weighted grid graph / Dijkstra / minimax path

Time Complexity:
O(N^2 log(N^2))

Space Complexity:
O(N^2)
"""

import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        size = len(grid)

        min_heap: list[tuple[int, int, int]] = [(grid[0][0], 0, 0)]
        visited: set[tuple[int, int]] = set()
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        while min_heap:
            time, row, col = heapq.heappop(min_heap)

            if (row, col) in visited:
                continue

            visited.add((row, col))

            if (row, col) == (size - 1, size - 1):
                return time

            for row_delta, col_delta in directions:
                next_row = row + row_delta
                next_col = col + col_delta

                if not (0 <= next_row < size and 0 <= next_col < size):
                    continue

                if (next_row, next_col) in visited:
                    continue

                next_time = max(time, grid[next_row][next_col])
                heapq.heappush(
                    min_heap,
                    (next_time, next_row, next_col),
                )

        return -1
