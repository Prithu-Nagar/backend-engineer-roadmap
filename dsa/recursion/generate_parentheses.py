"""
LeetCode 22
Generate Parentheses

Day 55 — Backtracking

Generate all well-formed combinations containing n pairs of parentheses.

Time Complexity:
O(4^n / sqrt(n)) for the number of generated combinations.

Space Complexity:
O(n) auxiliary recursion space, excluding the returned results.
"""

def generate_parenthesis(n: int) -> list[str]:
    """Return all well-formed parenthesis strings containing n pairs."""
    if n < 0:
        return []

    result: list[str] = []
    current: list[str] = []

    def backtrack(open_count: int, close_count: int) -> None:
        if len(current) == 2 * n:
            result.append("".join(current))
            return

        if open_count < n:
            current.append("(")
            backtrack(open_count + 1, close_count)
            current.pop()

        if close_count < open_count:
            current.append(")")
            backtrack(open_count, close_count + 1)
            current.pop()

    backtrack(0, 0)
    return result


if __name__ == "__main__":
    print(generate_parenthesis(3))
