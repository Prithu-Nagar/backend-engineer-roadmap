"""
Problem:
Shortest Path in a Binary Matrix

Pattern:
Graph BFS / shortest path in grid

Time Complexity:
O(n^2)

Space Complexity:
O(n^2)
"""

from collections import deque
from typing import List


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)

        if grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
            return -1

        if n == 1:
            return 1

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1),
        ]

        queue = deque([(0, 0, 1)])
        visited = {(0, 0)}

        while queue:
            row, col, steps = queue.popleft()

            for dr, dc in directions:
                next_row = row + dr
                next_col = col + dc

                if (
                    0 <= next_row < n
                    and 0 <= next_col < n
                    and (next_row, next_col) not in visited
                    and grid[next_row][next_col] == 0
                ):
                    if next_row == n - 1 and next_col == n - 1:
                        return steps + 1

                    visited.add((next_row, next_col))
                    queue.append((next_row, next_col, steps + 1))

        return -1
