"""
LeetCode 682
Baseball Game
"""


class Solution:
    def calPoints(self, operations: list[str]) -> int:

        stack = []

        for operation in operations:

            if operation == "+":
                stack.append(stack[-1] + stack[-2])

            elif operation == "D":
                stack.append(2 * stack[-1])

            elif operation == "C":
                stack.pop()

            else:
                stack.append(int(operation))

        return sum(stack)


if __name__ == "__main__":

    solution = Solution()

    operations = ["5", "2", "C", "D", "+"]

    print(solution.calPoints(operations))