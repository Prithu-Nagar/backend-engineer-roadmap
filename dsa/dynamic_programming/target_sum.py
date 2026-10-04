"""
LeetCode 494
Target Sum

Time Complexity:
O(n * total_sum)

Space Complexity:
O(total_sum)
"""


def find_target_sum_ways(nums: list[int], target: int) -> int:
    """Return the number of +/- assignments that reach target."""
    total = sum(nums)
    if abs(target) > total or (total + target) % 2:
        return 0

    subset_sum = (total + target) // 2
    dp = [0] * (subset_sum + 1)
    dp[0] = 1

    for number in nums:
        for current in range(subset_sum, number - 1, -1):
            dp[current] += dp[current - number]

    return dp[subset_sum]


if __name__ == "__main__":
    print(find_target_sum_ways([1, 1, 1, 1, 1], 3))
    print(find_target_sum_ways([1], 1))
