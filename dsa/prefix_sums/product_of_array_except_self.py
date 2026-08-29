"""
LeetCode: Product of Array Except Self

Pattern:
Prefix / Suffix Products

Time Complexity:
O(n)

Space Complexity:
O(1) extra space, excluding the output array
"""


class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        """Return the product of every value except the value at each index."""
        result = [1] * len(nums)

        prefix_product = 1
        for i, value in enumerate(nums):
            result[i] = prefix_product
            prefix_product *= value

        suffix_product = 1
        for i in range(len(nums) - 1, -1, -1):
            result[i] *= suffix_product
            suffix_product *= nums[i]

        return result
