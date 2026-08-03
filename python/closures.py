"""
LeetCode 141 - Linked List Cycle

Pattern:
Fast & Slow Pointer (Floyd's Cycle Detection)

Time Complexity: O(n)
Space Complexity: O(1)
"""


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class Solution:
    def hasCycle(self, head):
        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False


if __name__ == "__main__":
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)

    node1.next = node2
    node2.next = node3
    node3.next = node4

    # Create a cycle
    node4.next = node2

    solution = Solution()

    print("Contains Cycle:", solution.hasCycle(node1))