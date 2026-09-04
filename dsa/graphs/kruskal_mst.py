"""
Minimum Spanning Tree — Kruskal's Algorithm

Pattern:
Minimum spanning tree / Union-Find / greedy

Time Complexity:
O(E log E)

Space Complexity:
O(V + E)
"""

from typing import List


class DisjointSet:
    """Track connected components with path compression and union by rank."""

    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, node: int) -> int:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, first: int, second: int) -> bool:
        root_first = self.find(first)
        root_second = self.find(second)

        if root_first == root_second:
            return False

        if self.rank[root_first] < self.rank[root_second]:
            root_first, root_second = root_second, root_first

        self.parent[root_second] = root_first
        if self.rank[root_first] == self.rank[root_second]:
            self.rank[root_first] += 1
        return True


def kruskal_mst(n: int, edges: List[List[int]]) -> tuple[int, list[list[int]]]:
    """Return the MST total weight and selected edges for a connected graph."""
    if n <= 0:
        return 0, []

    dsu = DisjointSet(n)
    selected: list[list[int]] = []
    total_weight = 0

    for weight, first, second in sorted((w, u, v) for u, v, w in edges):
        if dsu.union(first, second):
            selected.append([first, second, weight])
            total_weight += weight
            if len(selected) == n - 1:
                break

    if len(selected) != n - 1:
        raise ValueError("graph must be connected to have an MST")

    return total_weight, selected


if __name__ == "__main__":
    graph_edges = [
        [0, 1, 4],
        [0, 2, 3],
        [1, 2, 1],
        [1, 3, 2],
        [2, 3, 4],
    ]
    print(kruskal_mst(4, graph_edges))
