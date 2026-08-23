"""
Problem: Lowest Common Ancestor of a Binary Search Tree
Pattern: BST Ordered Traversal
Time Complexity: O(h)
Space Complexity: O(1)
"""


class Solution:
    def lowestCommonAncestor(self, root, p, q):
        current = root

        while current:
            if p.val < current.val and q.val < current.val:
                current = current.left
            elif p.val > current.val and q.val > current.val:
                current = current.right
            else:
                return current

        return None
