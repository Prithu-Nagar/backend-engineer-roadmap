"""Day 86 — Mixed hard-pattern review.

Practice choosing an invariant, proving correctness, and testing edge cases.
These are compact reference implementations, not a substitute for timed attempts.
"""

from collections import defaultdict


def largest_rectangle_area(heights: list[int]) -> int:
    """Return the largest histogram rectangle area in O(n) time."""
    if any(height < 0 for height in heights):
        raise ValueError("heights must be non-negative")
    stack: list[int] = []
    best = 0
    for index in range(len(heights) + 1):
        current = heights[index] if index < len(heights) else 0
        while stack and heights[stack[-1]] > current:
            height = heights[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, height * (index - left))
        stack.append(index)
    return best


def min_window_substring(source: str, target: str) -> str:
    """Return the shortest source window containing target's character counts."""
    if not target:
        return ""
    required: dict[str, int] = defaultdict(int)
    for char in target:
        required[char] += 1
    missing = len(target)
    left = 0
    best_start, best_length = 0, float("inf")
    for right, char in enumerate(source):
        if required[char] > 0:
            missing -= 1
        required[char] -= 1
        while missing == 0:
            length = right - left + 1
            if length < best_length:
                best_start, best_length = left, length
            outgoing = source[left]
            required[outgoing] += 1
            if required[outgoing] > 0:
                missing += 1
            left += 1
    return "" if best_length == float("inf") else source[best_start:best_start + best_length]


def network_delay_time(edges: list[tuple[int, int, int]], n: int, source: int) -> int:
    """Dijkstra for positive weighted directed edges; return -1 if not all nodes reached."""
    import heapq

    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for start, end, weight in edges:
        if weight < 0:
            raise ValueError("Dijkstra requires non-negative edge weights")
        graph[start].append((end, weight))
    distances = {source: 0}
    heap = [(0, source)]
    while heap:
        distance, node = heapq.heappop(heap)
        if distance != distances[node]:
            continue
        for neighbor, weight in graph[node]:
            candidate = distance + weight
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return max(distances.values()) if len(distances) == n else -1


def run_smoke_tests() -> None:
    assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle_area([]) == 0
    assert min_window_substring("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window_substring("a", "aa") == ""
    assert network_delay_time([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2) == 2
    assert network_delay_time([(1, 2, 1)], 3, 1) == -1


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 86 DSA mixed hard-pattern checks passed.")
