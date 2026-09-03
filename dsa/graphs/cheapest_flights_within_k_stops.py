"""
Problem:
Cheapest Flights Within K Stops

Pattern:
Graph shortest path with a bounded number of stops

Time Complexity:
O(K * E log(K * V))

Space Complexity:
O(K * V + E)
"""

import heapq
from typing import List


class Solution:
    def findCheapestPrice(
        self,
        n: int,
        flights: List[List[int]],
        src: int,
        dst: int,
        k: int,
    ) -> int:
        graph: dict[int, list[tuple[int, int]]] = {node: [] for node in range(n)}

        for from_city, to_city, price in flights:
            graph[from_city].append((to_city, price))

        # A state includes the number of edges used because reaching the same
        # city with fewer stops can be more useful than reaching it more cheaply.
        max_edges = k + 1
        best: list[list[float]] = [
            [float("inf")] * (max_edges + 1) for _ in range(n)
        ]
        best[src][0] = 0

        min_heap: list[tuple[int, int, int]] = [(0, src, 0)]

        while min_heap:
            cost, city, edges_used = heapq.heappop(min_heap)

            if city == dst:
                return cost

            if cost > best[city][edges_used] or edges_used == max_edges:
                continue

            for neighbor, price in graph[city]:
                new_edges = edges_used + 1
                new_cost = cost + price

                if new_cost < best[neighbor][new_edges]:
                    best[neighbor][new_edges] = new_cost
                    heapq.heappush(min_heap, (new_cost, neighbor, new_edges))

        return -1
