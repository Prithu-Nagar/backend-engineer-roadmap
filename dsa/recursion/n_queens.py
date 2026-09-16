"""
LeetCode: N-Queens

Day 47 — Backtracking review

Place n queens on an n x n chessboard so that no two queens attack each
other. Track occupied columns and diagonals while building one row at a time.
"""

from typing import List


def solve_n_queens(n: int) -> List[List[str]]:
    """Return all valid N-Queens board configurations."""
    if n <= 0:
        return []

    result: List[List[str]] = []
    board = [["."] * n for _ in range(n)]
    columns: set[int] = set()
    diagonals: set[int] = set()  # row - col
    anti_diagonals: set[int] = set()  # row + col

    def backtrack(row: int) -> None:
        if row == n:
            result.append(["".join(board_row) for board_row in board])
            return

        for col in range(n):
            if col in columns:
                continue
            if row - col in diagonals or row + col in anti_diagonals:
                continue

            board[row][col] = "Q"
            columns.add(col)
            diagonals.add(row - col)
            anti_diagonals.add(row + col)

            backtrack(row + 1)

            board[row][col] = "."
            columns.remove(col)
            diagonals.remove(row - col)
            anti_diagonals.remove(row + col)

    backtrack(0)
    return result


if __name__ == "__main__":
    for solution in solve_n_queens(4):
        print("\n".join(solution))
        print()
