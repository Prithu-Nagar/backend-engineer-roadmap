"""
LeetCode 424 - Longest Repeating Character Replacement
Pattern: Variable Sliding Window + Frequency Map
"""

from collections import defaultdict


def character_replacement(s: str, k: int) -> int:
    """Return the longest window that can be made one repeated character."""
    counts = defaultdict(int)
    left = 0
    max_frequency = 0
    best = 0

    for right, char in enumerate(s):
        counts[char] += 1
        max_frequency = max(max_frequency, counts[char])

        while (right - left + 1) - max_frequency > k:
            counts[s[left]] -= 1
            left += 1

        best = max(best, right - left + 1)

    return best


if __name__ == "__main__":
    for source, k in [("ABAB", 2), ("AABABBA", 1), ("AAAA", 0)]:
        print(source, k, "->", character_replacement(source, k))
