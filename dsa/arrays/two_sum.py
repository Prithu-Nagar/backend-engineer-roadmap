"""
Problem:
Two Sum

Pattern:
HashMap

Time Complexity:
O(n)

Space Complexity:
O(n)
"""

class Solution:
    def twoSum(self, nums, target):
        hashmap = {}

        for i, num in enumerate(nums):
            complement = target - num

            if complement in hashmap:
                return [hashmap[complement], i]

            hashmap[num] = i