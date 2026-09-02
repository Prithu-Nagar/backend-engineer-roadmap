"""
LeetCode 63
Unique Paths II

Time Complexity:
O(m * n)

Space Complexity:
O(n)
"""


def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    """Return the number of paths that avoid blocked cells."""
    if not obstacle_grid or not obstacle_grid[0]:
        return 0

    columns = len(obstacle_grid[0])
    dp = [0] * columns
    dp[0] = 1

    for row in obstacle_grid:
        for col in range(columns):
            if row[col] == 1:
                dp[col] = 0
            elif col > 0:
                dp[col] += dp[col - 1]

    return dp[-1]


if __name__ == "__main__":
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]

    print(unique_paths_with_obstacles(grid))
