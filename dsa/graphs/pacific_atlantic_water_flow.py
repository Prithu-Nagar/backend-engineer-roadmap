"""
LeetCode: 417. Pacific Atlantic Water Flow
Day 58 — Mixed Medium
"""

from __future__ import annotations


def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    """Return cells from which water can flow to both oceans."""
    if not heights or not heights[0]:
        return []

    rows, cols = len(heights), len(heights[0])

    def reachable(starts: list[tuple[int, int]]) -> set[tuple[int, int]]:
        seen: set[tuple[int, int]] = set(starts)
        stack = list(starts)

        while stack:
            row, col = stack.pop()

            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = row + dr, col + dc

                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue

                if (nr, nc) in seen:
                    continue

                if heights[nr][nc] < heights[row][col]:
                    continue

                seen.add((nr, nc))
                stack.append((nr, nc))

        return seen

    pacific_starts = [
        *((row, 0) for row in range(rows)),
        *((0, col) for col in range(cols)),
    ]
    atlantic_starts = [
        *((row, cols - 1) for row in range(rows)),
        *((rows - 1, col) for col in range(cols)),
    ]

    both = reachable(pacific_starts) & reachable(atlantic_starts)
    return [[row, col] for row, col in sorted(both)]


if __name__ == "__main__":
    matrix = [
        [1, 2, 2, 3, 5],
        [3, 2, 3, 4, 4],
        [2, 4, 5, 3, 1],
        [6, 7, 1, 4, 5],
        [5, 1, 1, 2, 4],
    ]
    print(pacific_atlantic(matrix))
