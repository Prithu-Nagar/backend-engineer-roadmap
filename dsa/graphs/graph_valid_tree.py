"""Day 64 — Graph Valid Tree.

Interview pattern: Union-Find / connected components / cycle detection.
"""

from __future__ import annotations


class Solution:
    def validTree(self, n: int, edges: list[list[int]]) -> bool:
        """Return True when edges form exactly one tree over n vertices."""
        if n == 0:
            return False

        if len(edges) != n - 1:
            return False

        parent = list(range(n))
        rank = [0] * n

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        def union(left: int, right: int) -> bool:
            root_left = find(left)
            root_right = find(right)

            if root_left == root_right:
                return False

            if rank[root_left] < rank[root_right]:
                root_left, root_right = root_right, root_left

            parent[root_right] = root_left
            if rank[root_left] == rank[root_right]:
                rank[root_left] += 1

            return True

        return all(union(left, right) for left, right in edges)
