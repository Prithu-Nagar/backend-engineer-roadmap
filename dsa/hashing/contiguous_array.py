"""
LeetCode: Contiguous Array

Day 45 — Hashing + Prefix Sums review.
"""


def find_max_length(nums: list[int]) -> int:
    """Return the longest contiguous subarray with equal 0s and 1s."""
    first_seen = {0: -1}
    balance = 0
    best = 0

    for index, value in enumerate(nums):
        balance += -1 if value == 0 else 1

        if balance in first_seen:
            best = max(best, index - first_seen[balance])
        else:
            first_seen[balance] = index

    return best


if __name__ == "__main__":
    print(find_max_length([0, 1, 0]))
    print(find_max_length([0, 1, 0, 1]))
