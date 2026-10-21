"""Day 82: Dynamic Programming and backtracking interview review.

Run directly to execute the built-in smoke tests. Functions are intentionally
small so the state, transition, and pruning decisions remain easy to explain.
"""
from __future__ import annotations

from collections.abc import Sequence


def unique_paths_with_obstacles(grid: Sequence[Sequence[int]]) -> int:
    """Count paths through a grid where 1 marks a blocked cell.

    Time: O(rows * cols). Auxiliary space: O(cols).
    """
    if not grid or not grid[0]:
        return 0
    cols = len(grid[0])
    if any(len(row) != cols for row in grid):
        raise ValueError("grid must be rectangular")
    dp = [0] * cols
    dp[0] = 0 if grid[0][0] else 1
    for row in grid:
        for col, blocked in enumerate(row):
            if blocked:
                dp[col] = 0
            elif col:
                dp[col] += dp[col - 1]
    return dp[-1]


def combination_sum(candidates: Sequence[int], target: int) -> list[list[int]]:
    """Return unique combinations; each positive candidate may be reused.

    Time is exponential in the worst case. Auxiliary space is O(target/min
    candidate) for the recursion path, excluding returned combinations.
    """
    if target < 0:
        return []
    if any(value <= 0 for value in candidates):
        raise ValueError("candidates must be positive integers")
    values = sorted(set(candidates))
    results: list[list[int]] = []
    path: list[int] = []

    def search(start: int, remaining: int) -> None:
        if remaining == 0:
            results.append(path.copy())
            return
        for index in range(start, len(values)):
            value = values[index]
            if value > remaining:
                break
            path.append(value)
            search(index, remaining - value)
            path.pop()

    search(0, target)
    return results


def word_exists(board: Sequence[Sequence[str]], word: str) -> bool:
    """Return whether word can be formed by adjacent cells without reuse.

    Time: O(rows * cols * 4**len(word)) upper bound. Auxiliary space:
    O(len(word)) recursion depth, excluding the input board.
    """
    if not word:
        return True
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])
    if any(len(row) != cols for row in board):
        raise ValueError("board must be rectangular")

    def search(row: int, col: int, index: int) -> bool:
        if index == len(word):
            return True
        if (row < 0 or row >= rows or col < 0 or col >= cols
                or board[row][col] != word[index]):
            return False
        # Track visited cells in a set rather than mutating the caller's board.
        cell = (row, col)
        if cell in visited:
            return False
        visited.add(cell)
        found = any(search(row + dr, col + dc, index + 1)
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        visited.remove(cell)
        return found

    visited: set[tuple[int, int]] = set()
    return any(search(row, col, 0)
               for row in range(rows) for col in range(cols))


def run_smoke_tests() -> None:
    assert unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert unique_paths_with_obstacles([[1]]) == 0
    assert unique_paths_with_obstacles([]) == 0
    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert combination_sum([2], 1) == []
    assert word_exists([["A", "B", "C", "E"],
                        ["S", "F", "C", "S"],
                        ["A", "D", "E", "E"]], "ABCCED")
    assert not word_exists([["A", "B"], ["C", "D"]], "ABCA")
    try:
        combination_sum([0, 1], 2)
    except ValueError:
        pass
    else:
        raise AssertionError("non-positive candidates must fail")


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 82 DP/backtracking review passed.")
