"""
LeetCode: Permutation in String
Pattern: Fixed Sliding Window + Frequency Map
"""

from collections import Counter


def check_inclusion(s1: str, s2: str) -> bool:
    """Return True if s2 contains a permutation of s1."""
    if len(s1) > len(s2):
        return False

    required = Counter(s1)
    window = Counter()
    left = 0
    window_size = len(s1)

    for right, char in enumerate(s2):
        window[char] += 1

        if right - left + 1 > window_size:
            outgoing = s2[left]
            window[outgoing] -= 1

            if window[outgoing] == 0:
                del window[outgoing]

            left += 1

        if window == required:
            return True

    return False


if __name__ == "__main__":
    examples = [
        ("ab", "eidbaooo"),
        ("ab", "eidboaoo"),
        ("adc", "dcda"),
    ]

    for s1, s2 in examples:
        print(s1, s2, "->", check_inclusion(s1, s2))