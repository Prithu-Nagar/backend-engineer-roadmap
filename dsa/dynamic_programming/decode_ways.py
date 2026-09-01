"""
LeetCode 91
Decode Ways

Time Complexity:
O(n)

Space Complexity:
O(1)
"""


def num_decodings(s: str) -> int:
    """Return the number of valid decodings of a digit string."""
    if not s or s[0] == "0":
        return 0

    previous_two = 1
    previous_one = 1

    for index in range(1, len(s)):
        current = 0

        if s[index] != "0":
            current += previous_one

        two_digit = int(s[index - 1 : index + 1])
        if 10 <= two_digit <= 26:
            current += previous_two

        previous_two, previous_one = previous_one, current

        if previous_one == 0:
            return 0

    return previous_one


if __name__ == "__main__":
    print(num_decodings("226"))
