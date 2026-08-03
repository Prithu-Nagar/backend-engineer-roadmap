"""
LeetCode 206 - Reverse Linked List

Pattern:
Reverse Linked List

Time Complexity: O(n)
Space Complexity: O(1)
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head):
        prev = None
        current = head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        return prev


def create_linked_list(values):
    if not values:
        return None

    head = ListNode(values[0])
    current = head

    for value in values[1:]:
        current.next = ListNode(value)
        current = current.next

    return head


def print_linked_list(head):
    current = head

    while current:
        print(current.val, end="")
        if current.next:
            print(" -> ", end="")
        current = current.next

    print()


if __name__ == "__main__":
    head = create_linked_list([1, 2, 3, 4, 5])

    print("Original Linked List:")
    print_linked_list(head)

    reversed_head = Solution().reverseList(head)

    print("\nReversed Linked List:")
    print_linked_list(reversed_head)