"""
LeetCode: 98. Validate Binary Search Tree
Day 58 — Mixed Medium
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def is_valid_bst(root: TreeNode | None) -> bool:
    """Validate the BST ordering invariant using bounds."""
    def validate(node: TreeNode | None, lower: int | None, upper: int | None) -> bool:
        if node is None:
            return True

        if lower is not None and node.val <= lower:
            return False

        if upper is not None and node.val >= upper:
            return False

        return validate(node.left, lower, node.val) and validate(
            node.right, node.val, upper
        )

    return validate(root, None, None)


if __name__ == "__main__":
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    print(is_valid_bst(root))
