"""
LeetCode 392 - Is Subsequence

Difficulty : Easy
Pattern    : Two Pointers

Time Complexity  : O(n)
Space Complexity : O(1)
"""


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:

        i = 0
        j = 0

        while i < len(s) and j < len(t):

            if s[i] == t[j]:
                i += 1

            j += 1

        return i == len(s)