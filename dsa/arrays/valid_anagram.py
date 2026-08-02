"""
Problem:
Valid Anagram

Pattern:
HashMap

Time Complexity:
O(n)

Space Complexity:
O(n)
"""

class Solution:
    def isAnagram(self, s, t):

        if len(s) != len(t):
            return False

        count = {}

        for c in s:
            count[c] = count.get(c, 0) + 1

        for c in t:

            if c not in count:
                return False

            count[c] -= 1

            if count[c] == 0:
                del count[c]

        return len(count) == 0