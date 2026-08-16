"""
LeetCode 128 - Longest Consecutive Sequence
"""


def longest_consecutive(nums):
    values = set(nums)
    longest = 0

    for num in values:
        if num - 1 not in values:
            current = num
            length = 1

            while current + 1 in values:
                current += 1
                length += 1

            longest = max(longest, length)

    return longest


if __name__ == "__main__":
    print(longest_consecutive([100, 4, 200, 1, 3, 2]))