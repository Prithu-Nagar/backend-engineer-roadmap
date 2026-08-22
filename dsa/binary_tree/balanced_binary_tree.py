"""
Problem: Balanced Binary Tree
Pattern: Binary Tree / DFS / Recursive State
Time Complexity: O(n)
Space Complexity: O(h)
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def height(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0

            left_height = height(node.left)
            if left_height == -1:
                return -1

            right_height = height(node.right)
            if right_height == -1:
                return -1

            if abs(left_height - right_height) > 1:
                return -1

            return 1 + max(left_height, right_height)

        return height(root) != -1
