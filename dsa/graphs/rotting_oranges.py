"""
Problem:
Rotting Oranges

Pattern:
Graph traversal / BFS / Multi-source BFS

Time Complexity:
O(m * n)

Space Complexity:
O(m * n)
"""

from collections import deque


class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])

        queue = deque()
        fresh_oranges = 0

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 2:
                    queue.append((row, col))
                elif grid[row][col] == 1:
                    fresh_oranges += 1

        minutes = 0
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]

        while queue and fresh_oranges > 0:
            for _ in range(len(queue)):
                row, col = queue.popleft()

                for row_offset, col_offset in directions:
                    next_row = row + row_offset
                    next_col = col + col_offset

                    if (
                        next_row < 0
                        or next_row >= rows
                        or next_col < 0
                        or next_col >= cols
                        or grid[next_row][next_col] != 1
                    ):
                        continue

                    grid[next_row][next_col] = 2
                    fresh_oranges -= 1
                    queue.append((next_row, next_col))

            minutes += 1

        if fresh_oranges > 0:
            return -1

        return minutes