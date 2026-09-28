"""
LeetCode: 152. Maximum Product Subarray
Day 59 — Mixed Medium
"""

def max_product(nums: list[int]) -> int:
    """Return the maximum product of a contiguous subarray."""
    if not nums:
        raise ValueError("nums must not be empty")

    current_max = current_min = result = nums[0]

    for value in nums[1:]:
        if value < 0:
            current_max, current_min = current_min, current_max

        current_max = max(value, current_max * value)
        current_min = min(value, current_min * value)
        result = max(result, current_max)

    return result


if __name__ == "__main__":
    print(max_product([2, 3, -2, 4]))
