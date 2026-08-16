"""
LeetCode 560 - Subarray Sum Equals K
"""


def subarray_sum(nums, k):
    prefix_counts = {0: 1}

    current_sum = 0
    result = 0

    for num in nums:
        current_sum += num

        required = current_sum - k

        result += prefix_counts.get(required, 0)

        prefix_counts[current_sum] = (
            prefix_counts.get(current_sum, 0) + 1
        )

    return result


if __name__ == "__main__":
    print(subarray_sum([1, 1, 1], 2))