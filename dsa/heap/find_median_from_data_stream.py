"""
Find Median from Data Stream

Problem:
Median is the middle value in an ordered integer list. If the size of the list is even,
there is no middle value, and the median is the mean of the two middle values.

For example, for arr = [2,3,4], the median is 3.
For example, for arr = [2,3], the median is (2 + 3) / 2 = 2.5.

Implement a data structure that supports:
- addNum(num): Adds a number num from the data stream
- findMedian(): Returns the median of all elements so far

Approach:
- Use two heaps: max heap for smaller half, min heap for larger half
- Balance the heaps to maintain median
- Python heapq is a min heap, so negate values for max heap
"""

import heapq


class MedianFinder:
    """
    Find median from a stream of integers using two heaps.

    Time Complexity: addNum O(log n), findMedian O(1)
    Space Complexity: O(n)
    """

    def __init__(self):
        """Initialize two heaps."""
        self.small = []  # Max heap for smaller half (use negative values)
        self.large = []  # Min heap for larger half

    def addNum(self, num: int) -> None:
        """Add a number from the data stream."""
        # Add to max heap (small)
        heapq.heappush(self.small, -num)

        # Ensure every element in small is <= every element in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Maintain size property: len(small) >= len(large)
        if len(self.small) < len(self.large):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

        # Size difference should be at most 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

    def findMedian(self) -> float:
        """Return the median of all elements added so far."""
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0


if __name__ == "__main__":
    mf = MedianFinder()

    mf.addNum(1)
    print(f"Median after adding 1: {mf.findMedian()}")  # 1.0

    mf.addNum(2)
    print(f"Median after adding 2: {mf.findMedian()}")  # 1.5

    mf.addNum(3)
    print(f"Median after adding 3: {mf.findMedian()}")  # 2.0

    mf.addNum(4)
    print(f"Median after adding 4: {mf.findMedian()}")  # 2.5

    mf.addNum(5)
    print(f"Median after adding 5: {mf.findMedian()}")  # 3.0
