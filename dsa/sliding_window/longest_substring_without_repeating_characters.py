"""
LeetCode: Longest Substring Without Repeating Characters
Pattern: Variable Sliding Window + Set
"""


def length_of_longest_substring(s: str) -> int:
    """Return the length of the longest substring without duplicates."""
    seen = set()
    left = 0
    best = 0

    for right, char in enumerate(s):
        while char in seen:
            seen.remove(s[left])
            left += 1

        seen.add(char)
        best = max(best, right - left + 1)

    return best


if __name__ == "__main__":
    examples = ["abcabcbb", "bbbbb", "pwwkew", ""]

    for value in examples:
        print(value, "->", length_of_longest_substring(value))