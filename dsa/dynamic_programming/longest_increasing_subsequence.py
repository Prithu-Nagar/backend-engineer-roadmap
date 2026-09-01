"""
LeetCode 300
Longest Increasing Subsequence

Time Complexity:
O(n log n)

Space Complexity:
O(n)
"""

from bisect import bisect_left


def length_of_lis(nums: list[int]) -> int:
    """Return the length of the longest strictly increasing subsequence."""
    tails: list[int] = []

    for num in nums:
        index = bisect_left(tails, num)

        if index == len(tails):
            tails.append(num)
        else:
            tails[index] = num

    return len(tails)


if __name__ == "__main__":
    print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))
