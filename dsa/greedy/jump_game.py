"""
LeetCode: Jump Game

Pattern:
Greedy / farthest reachable position

Time Complexity:
O(N)

Space Complexity:
O(1)
"""


class Solution:
    def canJump(self, nums: list[int]) -> bool:
        """Return whether the final index is reachable."""
        farthest = 0

        for index, jump_length in enumerate(nums):
            if index > farthest:
                return False

            farthest = max(farthest, index + jump_length)

            if farthest >= len(nums) - 1:
                return True

        return True
