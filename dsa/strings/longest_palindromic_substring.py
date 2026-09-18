"""
Day 49 — Longest Palindromic Substring

Mixed timed-review problem: expand around every possible palindrome center.
"""

from __future__ import annotations


def longest_palindrome(s: str) -> str:
    """Return one longest palindromic substring."""

    if not s:
        return ""

    best_start = best_end = 0

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    for center in range(len(s)):
        left1, right1 = expand(center, center)
        left2, right2 = expand(center, center + 1)

        if right1 - left1 > best_end - best_start:
            best_start, best_end = left1, right1
        if right2 - left2 > best_end - best_start:
            best_start, best_end = left2, right2

    return s[best_start : best_end + 1]


if __name__ == "__main__":
    print(longest_palindrome("babad"))
