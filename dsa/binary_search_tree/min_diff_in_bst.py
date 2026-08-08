"""
Problem: Minimum Distance Between BST Nodes
Pattern: Inorder Traversal
Time Complexity: O(n)
Space Complexity: O(h)
"""


class Solution:
    def minDiffInBST(self, root):
        previous = None
        minimum = float("inf")

        def inorder(node):
            nonlocal previous, minimum

            if node is None:
                return

            inorder(node.left)

            if previous is not None:
                minimum = min(minimum, node.val - previous)

            previous = node.val

            inorder(node.right)

        inorder(root)

        return minimum