"""
Day 21 — Word Search

Backtracking pattern:
- Treat each cell as a possible starting point.
- Mark the current cell as visited.
- Explore four neighboring cells.
- Restore the cell before returning.

LeetCode: Word Search
"""

from typing import List


def exist(board: List[List[str]], word: str) -> bool:
    """Return True when ``word`` can be formed by adjacent board cells."""

    if not board or not board[0] or not word:
        return False

    rows = len(board)
    cols = len(board[0])

    def backtrack(row: int, col: int, index: int) -> bool:
        if index == len(word):
            return True

        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or board[row][col] != word[index]
        ):
            return False

        original = board[row][col]
        board[row][col] = "#"

        found = (
            backtrack(row + 1, col, index + 1)
            or backtrack(row - 1, col, index + 1)
            or backtrack(row, col + 1, index + 1)
            or backtrack(row, col - 1, index + 1)
        )

        board[row][col] = original  # Restore state for other paths.
        return found

    for row in range(rows):
        for col in range(cols):
            if backtrack(row, col, 0):
                return True

    return False


if __name__ == "__main__":
    board = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]

    print(exist(board, "ABCCED"))
