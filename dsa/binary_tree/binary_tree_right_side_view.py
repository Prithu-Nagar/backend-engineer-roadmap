"""Day 46 — Binary Tree Right Side View.

Interview pattern: level-order traversal and last-node selection per level.
"""

from __future__ import annotations

from collections import deque

class TreeNode:
    """Binary-tree node used by the solution."""

    def __init__(self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None):
        self.val = val
        self.left = left
        self.right = right


def right_side_view(root: TreeNode | None) -> list[int]:
    """Return the values visible when the tree is viewed from the right."""
    if root is None:
        return []

    result: list[int] = []
    queue = deque([root])

    while queue:
        level_size = len(queue)

        for index in range(level_size):
            node = queue.popleft()

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

            if index == level_size - 1:
                result.append(node.val)

    return result
