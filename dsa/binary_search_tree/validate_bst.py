"""
Problem: Validate Binary Search Tree
Pattern: Recursive Range Validation
Time Complexity: O(n)
Space Complexity: O(h)
"""


class Solution:
    def isValidBST(self, root):
        def validate(node, low, high):
            if node is None:
                return True

            if not (low < node.val < high):
                return False

            return (
                validate(node.left, low, node.val)
                and validate(node.right, node.val, high)
            )

        return validate(root, float("-inf"), float("inf"))