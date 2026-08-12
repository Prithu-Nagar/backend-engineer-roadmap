"""
LeetCode 64
Minimum Path Sum

Time Complexity:
O(m * n)

Space Complexity:
O(n)
"""

def min_path_sum(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        return 0

    rows = len(grid)
    cols = len(grid[0])

    dp = [0] * cols
    dp[0] = grid[0][0]

    for col in range(1, cols):
        dp[col] = dp[col - 1] + grid[0][col]

    for row in range(1, rows):
        dp[0] += grid[row][0]

        for col in range(1, cols):
            dp[col] = min(dp[col], dp[col - 1]) + grid[row][col]

    return dp[-1]


if __name__ == "__main__":
    grid = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1],
    ]

    print(min_path_sum(grid))