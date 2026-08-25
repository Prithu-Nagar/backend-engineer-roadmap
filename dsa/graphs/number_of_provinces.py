"""
Problem:
Number of Provinces

Pattern:
Graph / Union-Find / connected components

Time Complexity:
O(N^2 * alpha(N))

Space Complexity:
O(N)
"""


class Solution:
    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        n = len(isConnected)
        parent = list(range(n))
        size = [1] * n
        provinces = n

        def find(node: int) -> int:
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(first: int, second: int) -> bool:
            nonlocal provinces
            root_first = find(first)
            root_second = find(second)

            if root_first == root_second:
                return False

            if size[root_first] < size[root_second]:
                root_first, root_second = root_second, root_first

            parent[root_second] = root_first
            size[root_first] += size[root_second]
            provinces -= 1
            return True

        for first in range(n):
            for second in range(first + 1, n):
                if isConnected[first][second]:
                    union(first, second)

        return provinces
