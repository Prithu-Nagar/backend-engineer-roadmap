"""Day 46 — Lowest Common Ancestor of a Binary Tree.

Interview pattern: recursive tree search with post-order state aggregation.
"""

from __future__ import annotations


class TreeNode:
    """Binary-tree node used by the solution."""

    def __init__(self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(
    root: TreeNode | None,
    p: TreeNode,
    q: TreeNode,
) -> TreeNode | None:
    """Return the lowest node that is an ancestor of both p and q."""
    if root is None or root is p or root is q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left is not None and right is not None:
        return root

    return left or right
