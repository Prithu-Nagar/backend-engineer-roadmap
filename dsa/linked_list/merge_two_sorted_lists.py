"""
LeetCode 21 - Merge Two Sorted Lists

Pattern:
Two Pointers / Linked List

Time Complexity: O(n + m)
Space Complexity: O(1)
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, list1, list2):
        dummy = ListNode()
        current = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next

            current = current.next

        current.next = list1 if list1 else list2

        return dummy.next


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
    list1 = create_linked_list([1, 2, 4])
    list2 = create_linked_list([1, 3, 4])

    merged = Solution().mergeTwoLists(list1, list2)

    print("Merged Linked List:")
    print_linked_list(merged)
