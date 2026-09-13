"""
LeetCode: 33. Search in Rotated Sorted Array

Pattern:
Binary Search on a Rotated Sorted Array

Time Complexity:
O(log n)

Space Complexity:
O(1)
"""


def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


if __name__ == "__main__":
    examples = [
        ([4, 5, 6, 7, 0, 1, 2], 0),
        ([4, 5, 6, 7, 0, 1, 2], 3),
        ([1], 1),
    ]

    for nums, target in examples:
        print(f"Input:  nums={nums}, target={target}")
        print(f"Output: {search(nums, target)}")
        print()
