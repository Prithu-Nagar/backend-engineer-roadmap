"""
LeetCode 232
Implement Queue using Stacks

Time Complexity
---------------
push  : O(1)
pop   : Amortized O(1)
peek  : Amortized O(1)
empty : O(1)

Space Complexity
----------------
O(n)
"""


class MyQueue:

    def __init__(self):
        self.input_stack = []
        self.output_stack = []

    def push(self, x: int) -> None:
        self.input_stack.append(x)

    def pop(self) -> int:
        self._transfer()
        return self.output_stack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.output_stack[-1]

    def empty(self) -> bool:
        return not self.input_stack and not self.output_stack

    def _transfer(self):
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())