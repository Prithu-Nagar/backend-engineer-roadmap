"""
LeetCode: Subarray Sums Divisible by K

Day 45 — Prefix sums + hashing review.
"""


def subarrays_div_by_k(nums: list[int], k: int) -> int:
    """Count non-empty subarrays whose sum is divisible by k."""
    if k <= 0:
        raise ValueError("k must be positive")

    remainder_count = {0: 1}
    prefix_sum = 0
    result = 0

    for value in nums:
        prefix_sum += value
        remainder = prefix_sum % k

        result += remainder_count.get(remainder, 0)
        remainder_count[remainder] = remainder_count.get(remainder, 0) + 1

    return result


if __name__ == "__main__":
    print(subarrays_div_by_k([4, 5, 0, -2, -3, 1], 5))
