"""Day 88 — Targeted DSA repair based on Day 87 assessment results.

Run the smoke tests, then choose one or two functions whose pattern still
feels difficult. Record the missed invariant and re-solve without notes.
"""

from collections import deque
from collections.abc import Sequence


def two_sum(nums: Sequence[int], target: int) -> list[int]:
    """Return indices of a pair summing to target, or an empty list."""
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    return []


def longest_unique_substring(text: str) -> int:
    """Length of the longest substring with no repeated characters."""
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, char in enumerate(text):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        best = max(best, right - left + 1)
    return best


def level_order(root: dict | None) -> list[list[int]]:
    """BFS for nested nodes with value, left, and right keys."""
    if root is None:
        return []
    levels: list[list[int]] = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node["value"])
            if node.get("left") is not None:
                queue.append(node["left"])
            if node.get("right") is not None:
                queue.append(node["right"])
        levels.append(level)
    return levels


def can_finish(course_count: int, prerequisites: Sequence[tuple[int, int]]) -> bool:
    """Return whether all courses can be completed (Kahn's algorithm)."""
    if course_count < 0:
        raise ValueError("course_count cannot be negative")
    graph: list[list[int]] = [[] for _ in range(course_count)]
    indegree = [0] * course_count
    for course, prerequisite in prerequisites:
        if not (0 <= course < course_count and 0 <= prerequisite < course_count):
            raise ValueError("course index out of range")
        graph[prerequisite].append(course)
        indegree[course] += 1
    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    completed = 0
    while queue:
        node = queue.popleft()
        completed += 1
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return completed == course_count


def coin_change(coins: Sequence[int], amount: int) -> int:
    """Minimum coins for amount, or -1 when it cannot be formed."""
    if amount < 0:
        return -1
    if any(coin <= 0 for coin in coins):
        raise ValueError("coin denominations must be positive")
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for subtotal in range(1, amount + 1):
        for coin in coins:
            if coin <= subtotal:
                dp[subtotal] = min(dp[subtotal], dp[subtotal - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


def run_smoke_tests() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([1, 2], 8) == []
    assert longest_unique_substring("abcabcbb") == 3
    assert longest_unique_substring("") == 0
    assert level_order({"value": 1, "left": {"value": 2}, "right": None}) == [[1], [2]]
    assert level_order(None) == []
    assert can_finish(2, [(1, 0)])
    assert not can_finish(2, [(1, 0), (0, 1)])
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 88 DSA repair smoke tests passed.")
