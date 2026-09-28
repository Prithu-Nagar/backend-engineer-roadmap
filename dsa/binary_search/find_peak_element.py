"""
LeetCode: 162. Find Peak Element
Day 59 — Mixed Medium
"""

def find_peak_element(nums: list[int]) -> int:
    """Return an index of a peak element."""
    if not nums:
        raise ValueError("nums must not be empty")

    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[mid + 1]:
            right = mid
        else:
            left = mid + 1

    return left


if __name__ == "__main__":
    print(find_peak_element([1, 2, 1, 3, 5, 6, 4]))
