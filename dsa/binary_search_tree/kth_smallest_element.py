"""
Problem: Kth Smallest Element in a BST
Pattern: Inorder Traversal
Time Complexity: O(h + k)
Space Complexity: O(h)
"""


class Solution:
    def kthSmallest(self, root, k):
        stack = []
        current = root

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            k -= 1

            if k == 0:
                return current.val

            current = current.right

        return None
