import heapq
from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    frequencies = Counter(nums)

    min_heap = []

    for num, frequency in frequencies.items():
        heapq.heappush(min_heap, (frequency, num))

        if len(min_heap) > k:
            heapq.heappop(min_heap)

    return [num for _, num in min_heap]


if __name__ == "__main__":
    nums = [1, 1, 1, 2, 2, 3]
    k = 2

    print(top_k_frequent(nums, k))