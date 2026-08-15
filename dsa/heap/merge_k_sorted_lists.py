"""
Merge K Sorted Lists

Problem:
You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

Approach:
- Use a min heap to efficiently get the smallest node
- Push the head of each list into the heap
- Repeatedly pop the smallest node and add it to result
- Push the next node from the popped list into heap
"""

import heapq
from typing import Optional


class ListNode:
    """Definition for singly-linked list node."""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __lt__(self, other):
        """Define comparison for heap ordering."""
        return self.val < other.val


def mergeKLists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted linked lists using a min heap.

    Time Complexity: O(n log k) where n is total nodes, k is number of lists
    Space Complexity: O(k)
    """
    if not lists:
        return None

    # Create a min heap
    min_heap = []

    # Add the head of each list to heap
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst.val, i, lst))

    dummy = ListNode(0)
    current = dummy

    while min_heap:
        # Get the node with minimum value
        val, idx, node = heapq.heappop(min_heap)

        # Add it to result
        current.next = node
        current = current.next

        # Add the next node from the same list
        if node.next:
            heapq.heappush(min_heap, (node.next.val, idx, node.next))

    return dummy.next


def mergeKListsDivideConquer(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted lists using divide and conquer approach.

    Time Complexity: O(n log k)
    Space Complexity: O(log k) for recursion stack
    """
    if not lists:
        return None

    if len(lists) == 1:
        return lists[0]

    # Merge pairs of lists
    mid = len(lists) // 2
    left = mergeKListsDivideConquer(lists[:mid])
    right = mergeKListsDivideConquer(lists[mid:])

    return mergeTwoLists(left, right)


def mergeTwoLists(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    """Merge two sorted linked lists."""
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val < l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 if l1 else l2
    return dummy.next


if __name__ == "__main__":
    # Create sample lists
    l1 = ListNode(1, ListNode(4, ListNode(5)))
    l2 = ListNode(1, ListNode(3, ListNode(4)))
    l3 = ListNode(2, ListNode(6))

    lists = [l1, l2, l3]
    result = mergeKLists(lists)

    # Print result
    current = result
    output = []
    while current:
        output.append(current.val)
        current = current.next

    print(f"Merged list: {output}")
