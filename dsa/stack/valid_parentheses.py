"""
LeetCode 20
Valid Parentheses
"""

class Solution:
    def isValid(self, s: str) -> bool:

        stack = []

        mapping = {
            ')': '(',
            '}': '{',
            ']': '['
        }

        for ch in s:

            if ch in "([{":
                stack.append(ch)

            else:
                if not stack:
                    return False

                if stack[-1] != mapping[ch]:
                    return False

                stack.pop()

        return len(stack) == 0


if __name__ == "__main__":

    solution = Solution()

    print(solution.isValid("()"))
    print(solution.isValid("()[]{}"))
    print(solution.isValid("(]"))
    print(solution.isValid("([)]"))
    print(solution.isValid("{[]}"))