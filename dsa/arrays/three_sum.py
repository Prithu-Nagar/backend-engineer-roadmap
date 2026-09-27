"""
LeetCode: 15. 3Sum
Day 58 — Mixed Medium
"""

from __future__ import annotations


def three_sum(nums: list[int]) -> list[list[int]]:
    """Return unique triplets whose values sum to zero."""
    nums.sort()
    result: list[list[int]] = []

    for left in range(len(nums) - 2):
        if nums[left] > 0:
            break

        if left > 0 and nums[left] == nums[left - 1]:
            continue

        middle = left + 1
        right = len(nums) - 1

        while middle < right:
            total = nums[left] + nums[middle] + nums[right]

            if total < 0:
                middle += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[left], nums[middle], nums[right]])
                middle += 1
                right -= 1

                while middle < right and nums[middle] == nums[middle - 1]:
                    middle += 1

                while middle < right and nums[right] == nums[right + 1]:
                    right -= 1

    return result


if __name__ == "__main__":
    print(three_sum([-1, 0, 1, 2, -1, -4]))
