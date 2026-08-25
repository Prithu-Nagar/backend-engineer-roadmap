"""
Union-Find / Disjoint Set Union (DSU)

Supports efficient connectivity queries and set merging using
path compression and union by size.

Time Complexity:
- find: Amortized O(alpha(N))
- union: Amortized O(alpha(N))

Space Complexity:
O(N)
"""


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, node: int) -> int:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, first: int, second: int) -> bool:
        root_first = self.find(first)
        root_second = self.find(second)

        if root_first == root_second:
            return False

        if self.size[root_first] < self.size[root_second]:
            root_first, root_second = root_second, root_first

        self.parent[root_second] = root_first
        self.size[root_first] += self.size[root_second]
        return True


if __name__ == "__main__":
    dsu = UnionFind(5)
    dsu.union(0, 1)
    dsu.union(1, 2)
    print(dsu.find(0) == dsu.find(2))
    print(dsu.find(0) == dsu.find(3))
