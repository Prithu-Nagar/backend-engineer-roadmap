"""Day 87 — Full timed DSA assessment.

Suggested time: 60 minutes. Attempt without notes, explain invariants, and
record complexity before checking the smoke tests.
"""

from collections import deque


def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    return []


def longest_unique_substring(text: str) -> int:
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, char in enumerate(text):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        best = max(best, right - left + 1)
    return best


def level_order(root: dict | None) -> list[list[int]]:
    """Traverse a simple tree node dict: value, left, right."""
    if root is None:
        return []
    result: list[list[int]] = []
    queue = deque([root])
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node["value"])
            if node.get("left") is not None:
                queue.append(node["left"])
            if node.get("right") is not None:
                queue.append(node["right"])
        result.append(level)
    return result


def can_finish_courses(
    course_count: int, prerequisites: list[list[int]]
) -> bool:
    graph = [[] for _ in range(course_count)]
    indegree = [0] * course_count
    for course, prerequisite in prerequisites:
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


def coin_change(coins: list[int], amount: int) -> int:
    if amount < 0:
        return -1
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for subtotal in range(1, amount + 1):
        for coin in coins:
            if coin > 0 and coin <= subtotal:
                dp[subtotal] = min(dp[subtotal], dp[subtotal - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


def run_smoke_tests() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert longest_unique_substring("abcabcbb") == 3
    tree = {"value": 1, "left": {"value": 2}, "right": {"value": 3}}
    assert level_order(tree) == [[1], [2, 3]]
    assert can_finish_courses(2, [[1, 0]])
    assert not can_finish_courses(2, [[1, 0], [0, 1]])
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 87 DSA assessment smoke tests passed.")
