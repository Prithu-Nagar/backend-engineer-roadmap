"""
LeetCode 155
Min Stack
"""

class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:

        self.stack.append(val)

        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:

        value = self.stack.pop()

        if value == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


if __name__ == "__main__":

    obj = MinStack()

    obj.push(-2)
    obj.push(0)
    obj.push(-3)

    print("Minimum:", obj.getMin())

    obj.pop()

    print("Top:", obj.top())

    print("Minimum:", obj.getMin())