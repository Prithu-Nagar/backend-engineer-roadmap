import heapq


def find_kth_largest(nums: list[int], k: int) -> int:
    min_heap = nums[:k]
    heapq.heapify(min_heap)

    for num in nums[k:]:
        if num > min_heap[0]:
            heapq.heapreplace(min_heap, num)

    return min_heap[0]


if __name__ == "__main__":
    nums = [3, 2, 1, 5, 6, 4]
    k = 2

    print(find_kth_largest(nums, k))