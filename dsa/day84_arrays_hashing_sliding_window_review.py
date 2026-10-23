"""Day 84 — Arrays, hashing, and sliding-window interview review."""

from __future__ import annotations

from collections import Counter


def two_sum(nums: list[int], target: int) -> list[int]:
    """Return indices of two distinct values whose sum equals target."""
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    return []


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words by their character-frequency signature."""
    groups: dict[tuple[int, ...], list[str]] = {}
    for word in words:
        counts = [0] * 26
        for char in word:
            if not ("a" <= char <= "z"):
                raise ValueError("words must contain lowercase English letters")
            counts[ord(char) - ord("a")] += 1
        groups.setdefault(tuple(counts), []).append(word)
    return list(groups.values())


def longest_unique_substring_length(text: str) -> int:
    """Return the longest substring length with no repeated characters."""
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, char in enumerate(text):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        best = max(best, right - left + 1)
    return best


def max_sum_subarray_of_size_k(nums: list[int], k: int) -> int:
    """Return the maximum sum among contiguous windows of exactly k items."""
    if k <= 0 or k > len(nums):
        raise ValueError("k must be between 1 and len(nums)")
    window_sum = sum(nums[:k])
    best = window_sum
    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]
        best = max(best, window_sum)
    return best


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Return up to k most frequent values; ties follow Counter's order."""
    if k < 0:
        raise ValueError("k must be non-negative")
    return [value for value, _ in Counter(nums).most_common(k)]


def run_smoke_tests() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([1, 2], 7) == []
    grouped = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert sorted(sorted(group) for group in grouped) == [
        ["ate", "eat", "tea"], ["bat"], ["nat", "tan"]
    ]
    assert longest_unique_substring_length("abcabcbb") == 3
    assert longest_unique_substring_length("") == 0
    assert max_sum_subarray_of_size_k([2, 1, 5, 1, 3, 2], 3) == 9
    assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]


if __name__ == "__main__":
    run_smoke_tests()
    print("Day 84 DSA review checks passed.")
