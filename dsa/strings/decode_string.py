"""
LeetCode: 394. Decode String
Day 59 — Mixed Medium
"""

def decode_string(s: str) -> str:
    """Decode nested k[encoded_string] expressions."""
    count_stack: list[int] = []
    string_stack: list[str] = []
    current = []
    number = 0

    for char in s:
        if char.isdigit():
            number = number * 10 + int(char)
        elif char == "[":
            count_stack.append(number)
            string_stack.append("".join(current))
            number = 0
            current = []
        elif char == "]":
            repeat = count_stack.pop()
            prefix = string_stack.pop()
            current = [prefix + "".join(current) * repeat]
        else:
            current.append(char)

    return "".join(current)


if __name__ == "__main__":
    print(decode_string("3[a2[c]]"))
