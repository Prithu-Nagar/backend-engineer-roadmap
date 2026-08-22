"""
Problem: Diameter of Binary Tree
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
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0

        def height(node: Optional[TreeNode]) -> int:
            nonlocal diameter

            if node is None:
                return 0

            left_height = height(node.left)
            right_height = height(node.right)

            diameter = max(diameter, left_height + right_height)

            return 1 + max(left_height, right_height)

        height(root)
        return diameter
