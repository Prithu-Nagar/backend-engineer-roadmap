"""
Problem:
Network Delay Time

Pattern:
Graph shortest path / Dijkstra / BFS with priority queue

Time Complexity:
O((N + E) log N)

Space Complexity:
O(N + E)
"""

import heapq
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph: dict[int, list[tuple[int, int]]] = {node: [] for node in range(1, n + 1)}

        for u, v, w in times:
            graph[u].append((v, w))

        distances = {node: float("inf") for node in range(1, n + 1)}
        distances[k] = 0
        min_heap: list[tuple[int, int]] = [(0, k)]

        while min_heap:
            current_distance, node = heapq.heappop(min_heap)

            if current_distance > distances[node]:
                continue

            for neighbor, weight in graph[node]:
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(min_heap, (new_distance, neighbor))

        max_time = max(distances.values())
        return -1 if max_time == float("inf") else max_time
