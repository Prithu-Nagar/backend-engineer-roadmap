"""
Day 51 — Longest Palindromic Subsequence

Use interval-style dynamic programming to find the longest subsequence that
reads the same from left to right and right to left.
"""


def longest_palindromic_subsequence(text: str) -> int:
    """Return the length of the longest palindromic subsequence.

    Time: O(n^2)
    Space: O(n)
    """
    if not text:
        return 0

    dp = [1] * len(text)

    for left in range(len(text) - 2, -1, -1):
        previous_diagonal = 0
        for right in range(left + 1, len(text)):
            saved = dp[right]

            if text[left] == text[right]:
                dp[right] = previous_diagonal + 2
            else:
                dp[right] = max(dp[right], dp[right - 1])

            previous_diagonal = saved

    return dp[-1]


if __name__ == "__main__":
    print(longest_palindromic_subsequence("bbbab"))
