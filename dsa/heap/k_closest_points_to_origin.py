"""
K Closest Points to Origin

Problem:
Given an array of points where points[i] = [xi, yi] represent a point on the X-Y plane
and an integer k, return the k closest points to the origin (0, 0).

Approach:
- Use a max heap to maintain k closest points
- Calculate distance from origin for each point
- Use heapq with negative distances (Python has min heap)
- Return the k points with minimum distance
"""

import heapq


def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Find k closest points to origin using a max heap approach.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """

    def distance(point):
        """Calculate squared distance from origin."""
        return point[0] ** 2 + point[1] ** 2

    # Use negative distances for max heap behavior
    max_heap = []

    for point in points:
        dist = distance(point)

        if len(max_heap) < k:
            heapq.heappush(max_heap, (-dist, point))
        elif dist < -max_heap[0][0]:
            heapq.heapreplace(max_heap, (-dist, point))

    return [point for _, point in max_heap]


def kClosestSorted(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Alternative approach: Sort by distance and return first k.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    points.sort(key=lambda p: p[0] ** 2 + p[1] ** 2)
    return points[:k]


if __name__ == "__main__":
    points = [[1, 3], [-2, 2], [2, -2]]
    k = 2

    result = kClosest(points, k)
    print(f"K closest points: {result}")

    # Example 2
    points2 = [[3, 3], [5, -1], [-2, 4]]
    k2 = 2

    result2 = kClosest(points2, k2)
    print(f"K closest points: {result2}")
