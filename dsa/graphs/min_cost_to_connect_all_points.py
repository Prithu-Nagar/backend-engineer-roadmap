"""
LeetCode: Min Cost to Connect All Points

Pattern:
Minimum spanning tree / Kruskal / Union-Find

Time Complexity:
O(N^2 log N)

Space Complexity:
O(N^2)
"""

from typing import List

from dsa.graphs.kruskal_mst import DisjointSet


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0

        edges: list[tuple[int, int, int]] = []
        for first in range(n):
            x1, y1 = points[first]
            for second in range(first + 1, n):
                x2, y2 = points[second]
                distance = abs(x1 - x2) + abs(y1 - y2)
                edges.append((distance, first, second))

        edges.sort()
        dsu = DisjointSet(n)
        total = 0
        used = 0

        for distance, first, second in edges:
            if dsu.union(first, second):
                total += distance
                used += 1
                if used == n - 1:
                    break

        return total
