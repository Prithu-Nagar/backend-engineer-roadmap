"""
LeetCode 1143
Longest Common Subsequence

Time Complexity:
O(m * n)

Space Complexity:
O(n)
"""

def longest_common_subsequence(text1: str, text2: str) -> int:
    if not text1 or not text2:
        return 0

    if len(text1) < len(text2):
        text1, text2 = text2, text1

    dp = [0] * (len(text2) + 1)

    for i in range(1, len(text1) + 1):
        previous_diagonal = 0

        for j in range(1, len(text2) + 1):
            current = dp[j]

            if text1[i - 1] == text2[j - 1]:
                dp[j] = previous_diagonal + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])

            previous_diagonal = current

    return dp[-1]


if __name__ == "__main__":
    print(longest_common_subsequence("abcde", "ace"))