"""
LeetCode: 34. Find First and Last Position of Element in Sorted Array

Pattern:
Binary Search for Boundaries

Time Complexity:
O(log n)

Space Complexity:
O(1)
"""


def search_range(nums: list[int], target: int) -> list[int]:
    def find_boundary(find_first: bool) -> int:
        left, right = 0, len(nums) - 1
        boundary = -1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                boundary = mid
                if find_first:
                    right = mid - 1
                else:
                    left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return boundary

    return [find_boundary(True), find_boundary(False)]


if __name__ == "__main__":
    examples = [
        ([5, 7, 7, 8, 8, 10], 8),
        ([5, 7, 7, 8, 8, 10], 6),
        ([], 0),
    ]

    for nums, target in examples:
        print(f"Input:  nums={nums}, target={target}")
        print(f"Output: {search_range(nums, target)}")
        print()
