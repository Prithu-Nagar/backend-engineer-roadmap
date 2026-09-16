"""
LeetCode: Palindrome Partitioning

Day 47 — Backtracking review

Partition a string so every selected substring is a palindrome. The
backtracking state is the next unprocessed index plus the current partition.
"""

from typing import List


def partition(s: str) -> List[List[str]]:
    """Return all palindrome partitions of s."""
    result: List[List[str]] = []
    current: List[str] = []

    def is_palindrome(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    def backtrack(start: int) -> None:
        if start == len(s):
            result.append(current.copy())
            return

        for end in range(start, len(s)):
            if not is_palindrome(start, end):
                continue

            current.append(s[start : end + 1])
            backtrack(end + 1)
            current.pop()

    backtrack(0)
    return result


if __name__ == "__main__":
    print(partition("aab"))
