"""
Problem: Search in a Binary Search Tree
Pattern: Binary Search Tree Traversal
Time Complexity: O(h)
Space Complexity: O(1)
"""


class Solution:
    def searchBST(self, root, val):
        current = root

        while current:
            if current.val == val:
                return current

            if val < current.val:
                current = current.left
            else:
                current = current.right

        return None