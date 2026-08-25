"""
Problem:
Redundant Connection

Pattern:
Graph / Union-Find / cycle detection

Time Complexity:
O(N * alpha(N))

Space Complexity:
O(N)
"""


class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        n = len(edges)
        parent = list(range(n + 1))
        size = [1] * (n + 1)

        def find(node: int) -> int:
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        for first, second in edges:
            root_first = find(first)
            root_second = find(second)

            if root_first == root_second:
                return [first, second]

            if size[root_first] < size[root_second]:
                root_first, root_second = root_second, root_first

            parent[root_second] = root_first
            size[root_first] += size[root_second]

        return []
