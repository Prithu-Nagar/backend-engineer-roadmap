"""
Day 51 — Product of Array Except Self

Return an array where each position contains the product of every input
value except the value at that position.
"""


def product_except_self(nums: list[int]) -> list[int]:
    """Return products without using division.

    Time: O(n)
    Space: O(1) extra space excluding the output array.
    """
    result = [1] * len(nums)

    prefix = 1
    for index, value in enumerate(nums):
        result[index] = prefix
        prefix *= value

    suffix = 1
    for index in range(len(nums) - 1, -1, -1):
        result[index] *= suffix
        suffix *= nums[index]

    return result


if __name__ == "__main__":
    print(product_except_self([1, 2, 3, 4]))
