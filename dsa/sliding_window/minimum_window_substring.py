"""
LeetCode 76 - Minimum Window Substring
Pattern: Variable Sliding Window + Frequency Map
"""

from collections import Counter


def min_window(s: str, t: str) -> str:
    """Return the smallest substring of s containing every char from t."""
    if not s or not t:
        return ""

    required = Counter(t)
    window = Counter()
    formed = 0
    required_kinds = len(required)
    left = 0
    best = ""

    for right, char in enumerate(s):
        window[char] += 1
        if char in required and window[char] == required[char]:
            formed += 1

        while formed == required_kinds and left <= right:
            candidate = s[left : right + 1]
            if not best or len(candidate) < len(best):
                best = candidate

            outgoing = s[left]
            window[outgoing] -= 1
            if outgoing in required and window[outgoing] < required[outgoing]:
                formed -= 1
            left += 1

    return best


if __name__ == "__main__":
    examples = [("ADOBECODEBANC", "ABC"), ("a", "a"), ("a", "aa")]
    for source, target in examples:
        print(source, target, "->", min_window(source, target))
