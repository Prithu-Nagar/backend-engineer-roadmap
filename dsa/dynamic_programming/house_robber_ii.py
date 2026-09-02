"""
LeetCode 213
House Robber II

Time Complexity:
O(n)

Space Complexity:
O(1)
"""


def rob_linear(nums: list[int]) -> int:
    """Return the best robbery amount for a linear list of houses."""
    previous = 0
    current = 0

    for amount in nums:
        previous, current = current, max(current, previous + amount)

    return current


def rob(nums: list[int]) -> int:
    """Return the best robbery amount when houses form a circle."""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    # In a circle, the first and last houses cannot both be selected.
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


if __name__ == "__main__":
    print(rob([2, 3, 2]))
    print(rob([1, 2, 3, 1]))
