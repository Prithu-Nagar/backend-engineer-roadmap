"""LeetCode: Word Break

Day 42 — Dynamic Programming mixed review.
"""

from __future__ import annotations


def word_break(s: str, word_dict: list[str]) -> bool:
    """Return whether ``s`` can be segmented into dictionary words."""
    words = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True

    for end in range(1, len(s) + 1):
        for start in range(end):
            if dp[start] and s[start:end] in words:
                dp[end] = True
                break

    return dp[len(s)]
