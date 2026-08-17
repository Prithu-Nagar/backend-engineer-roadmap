"""
LeetCode: Minimum Size Subarray Sum
Pattern: Variable Sliding Window + Running Sum
"""


def min_sub_array_len(target: int, nums: list[int]) -> int:
    """Return the minimum length of a contiguous subarray with sum >= target."""
    left = 0
    window_sum = 0
    best = len(nums) + 1

    for right, value in enumerate(nums):
        window_sum += value

        while window_sum >= target:
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1

    return 0 if best == len(nums) + 1 else best


if __name__ == "__main__":
    examples = [
        (7, [2, 3, 1, 2, 4, 3]),
        (4, [1, 4, 4]),
        (11, [1, 1, 1, 1]),
    ]

    for target, nums in examples:
        print(target, nums, "->", min_sub_array_len(target, nums))