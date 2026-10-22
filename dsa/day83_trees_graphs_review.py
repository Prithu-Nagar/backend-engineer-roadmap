"""Day 83 — Trees and Graphs Interview Review.

Run directly to execute the smoke tests. Implementations are intentionally
small and focused on common interview patterns.
"""

from __future__ import annotations

from collections import deque


class TreeNode:
    """Binary-tree node used by the review exercises."""

    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def level_order(root: TreeNode | None) -> list[list[int]]:
    """Return binary-tree values grouped by depth using BFS."""
    if root is None:
        return []
    result: list[list[int]] = []
    queue = deque([root])
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


def is_valid_bst(root: TreeNode | None) -> bool:
    """Validate strict BST ordering with lower and upper bounds."""
    def validate(node: TreeNode | None, low: float, high: float) -> bool:
        if node is None:
            return True
        if not low < node.val < high:
            return False
        return validate(node.left, low, node.val) and validate(
            node.right, node.val, high
        )

    return validate(root, float("-inf"), float("inf"))


def count_components(vertex_count: int, edges: list[tuple[int, int]]) -> int:
    """Count connected components in an undirected graph using DFS."""
    if vertex_count < 0:
        raise ValueError("vertex_count must be non-negative")
    adjacency = [[] for _ in range(vertex_count)]
    for left, right in edges:
        if not (0 <= left < vertex_count and 0 <= right < vertex_count):
            raise ValueError("edge endpoint is outside the graph")
        adjacency[left].append(right)
        adjacency[right].append(left)

    seen: set[int] = set()
    components = 0
    for vertex in range(vertex_count):
        if vertex in seen:
            continue
        components += 1
        stack = [vertex]
        seen.add(vertex)
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return components


def can_finish_courses(
    course_count: int, prerequisites: list[tuple[int, int]]
) -> bool:
    """Return whether all courses can be completed (Kahn's algorithm)."""
    if course_count < 0:
        raise ValueError("course_count must be non-negative")
    adjacency = [[] for _ in range(course_count)]
    indegree = [0] * course_count
    for course, prerequisite in prerequisites:
        if not (0 <= course < course_count and 0 <= prerequisite < course_count):
            raise ValueError("course index is outside the graph")
        adjacency[prerequisite].append(course)
        indegree[course] += 1

    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    completed = 0
    while queue:
        current = queue.popleft()
        completed += 1
        for neighbor in adjacency[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return completed == course_count


def run_smoke_tests() -> None:
    root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6))
    assert level_order(root) == [[4], [2, 6], [1, 3]]
    assert is_valid_bst(root)
    assert not is_valid_bst(TreeNode(5, TreeNode(1), TreeNode(4)))
    assert level_order(None) == []
    assert count_components(5, [(0, 1), (1, 2), (3, 4)]) == 2
    assert count_components(0, []) == 0
    assert can_finish_courses(2, [(1, 0)])
    assert not can_finish_courses(2, [(1, 0), (0, 1)])


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 83 trees/graphs review passed.")
