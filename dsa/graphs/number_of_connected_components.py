"""Day 64 — Number of Connected Components in an Undirected Graph.

Interview pattern: graph traversal / connected components.
"""

from __future__ import annotations


class Solution:
    def countComponents(self, n: int, edges: list[list[int]]) -> int:
        """Return the number of connected components using DFS."""
        graph: list[list[int]] = [[] for _ in range(n)]

        for left, right in edges:
            graph[left].append(right)
            graph[right].append(left)

        visited = [False] * n
        components = 0

        def dfs(node: int) -> None:
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor)

        for node in range(n):
            if not visited[node]:
                components += 1
                dfs(node)

        return components
