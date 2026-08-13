"""
Problem:
Flood Fill

Pattern:
Graph traversal / DFS / BFS

Time Complexity:
O(m * n)

Space Complexity:
O(m * n)
"""


class Solution:
    def floodFill(
        self,
        image: list[list[int]],
        sr: int,
        sc: int,
        color: int,
    ) -> list[list[int]]:
        original_color = image[sr][sc]

        if original_color == color:
            return image

        rows = len(image)
        cols = len(image[0])

        def dfs(row: int, col: int) -> None:
            if (
                row < 0
                or row >= rows
                or col < 0
                or col >= cols
                or image[row][col] != original_color
            ):
                return

            image[row][col] = color

            dfs(row + 1, col)
            dfs(row - 1, col)
            dfs(row, col + 1)
            dfs(row, col - 1)

        dfs(sr, sc)

        return image