"""
Problem: Guess Number Higher or Lower
Pattern: Binary Search

Time Complexity: O(log n)
Space Complexity: O(1)
"""

# The guess API is already defined for you.
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n):
        left = 1
        right = n

        while left <= right:
            mid = left + (right - left) // 2

            result = guess(mid)

            if result == 0:
                return mid
            elif result < 0:
                right = mid - 1
            else:
                left = mid + 1