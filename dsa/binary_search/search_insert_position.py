"""
Problem: Search Insert Position
Pattern: Binary Search

Time Complexity: O(log n)
Space Complexity: O(1)
"""

class Solution:
    def searchInsert(self, nums, target):
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            elif nums[mid] < target:
                left = mid + 1

            else:
                right = mid - 1

        return left