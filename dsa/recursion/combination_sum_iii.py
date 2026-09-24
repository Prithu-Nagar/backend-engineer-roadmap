"""
LeetCode 216
Combination Sum III

Day 55 — Backtracking

Choose exactly k distinct numbers from 1 through 9 whose sum is n.

Time Complexity:
O(C(9, k) * k)

Space Complexity:
O(k) auxiliary recursion space, excluding the returned results.
"""

def combination_sum3(k: int, n: int) -> list[list[int]]:
    """Return combinations of k distinct digits from 1..9 that sum to n."""
    result: list[list[int]] = []
    current: list[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if len(current) == k:
            if remaining == 0:
                result.append(current.copy())
            return

        numbers_needed = k - len(current)
        if 9 - start + 1 < numbers_needed:
            return

        for value in range(start, 10):
            if value > remaining:
                break

            current.append(value)
            backtrack(value + 1, remaining - value)
            current.pop()

    if k <= 0 or k > 9 or n <= 0:
        return []

    backtrack(1, n)
    return result


if __name__ == "__main__":
    print(combination_sum3(3, 7))
    print(combination_sum3(3, 9))
