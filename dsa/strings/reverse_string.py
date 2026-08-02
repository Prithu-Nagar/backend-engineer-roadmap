"""
LeetCode 344 - Reverse String

Difficulty : Easy
Pattern    : Two Pointers

Time Complexity  : O(n)
Space Complexity : O(1)
"""


class Solution:
    def reverseString(self, s) -> None:

        left = 0
        right = len(s) - 1

        while left < right:

            s[left], s[right] = s[right], s[left]

            left += 1
            right -= 1