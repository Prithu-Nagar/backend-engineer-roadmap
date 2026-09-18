"""
Day 49 — Binary Tree Zigzag Level Order Traversal

Mixed timed-review problem: perform BFS while alternating the direction in
which each level is recorded.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    """Return binary-tree levels in alternating left/right order."""

    if root is None:
        return []

    result: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])
    left_to_right = True

    while queue:
        level = [node.val for node in queue]
        result.append(level if left_to_right else level[::-1])

        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        left_to_right = not left_to_right

    return result


if __name__ == "__main__":
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    print(zigzag_level_order(root))
