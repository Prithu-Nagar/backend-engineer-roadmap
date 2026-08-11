"""
LeetCode 198 - House Robber

Topic:
Dynamic Programming - 1D DP
"""

class Solution:
    def rob(self, nums: list[int]) -> int:
        if not nums:
            return 0

        if len(nums) == 1:
            return nums[0]

        previous = nums[0]
        current = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            previous, current = (
                current,
                max(current, previous + nums[i]),
            )

        return current

if __name__ == "__main__":
    solution = Solution()

    print(solution.rob([2, 7, 9, 3, 1]))
    print(solution.rob([1, 2, 3, 1]))
