"""
LeetCode 62
Unique Paths

Time Complexity:
O(m * n)

Space Complexity:
O(n)
"""

def unique_paths(m: int, n: int) -> int:
    dp = [1] * n

    for _ in range(1, m):
        for col in range(1, n):
            dp[col] += dp[col - 1]

    return dp[-1]


if __name__ == "__main__":
    print(unique_paths(3, 7))