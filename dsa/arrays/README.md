# Arrays

This directory contains LeetCode problems focused on array manipulation, hashing, and traversal techniques.

---

## Problems Solved

- Two Sum
- Contains Duplicate
- Valid Anagram

---

## Concepts Covered

- Array Traversal
- HashMap
- HashSet
- Frequency Counting
- Brute Force vs Optimized Approach
- Time & Space Complexity Analysis

---

## Interview Patterns

- Hashing
- Frequency Counting
- Lookup Tables
- Prefix/Suffix Traversal

---

## Additional Array Problems Already Present

- Best Time to Buy and Sell Stock — covered in the greedy pattern folder
- Product of Array Except Self — `../prefix_sums/product_of_array_except_self.py`
- Maximum Subarray — `maximum_subarray.py`
- Top K Frequent Elements — `../heap/top_k_frequent_elements.py`
- Longest Consecutive Sequence — `../hashing/longest_consecutive_sequence.py`

The repository organizes some problems by their primary solving pattern, so
not every array-related solution is stored in this directory.

---

## Day 58 — 3Sum

Added `three_sum.py`.

Topics:

- Sorting before two-pointer traversal
- Duplicate skipping
- Fixed-index + two-pointer search
- O(n²) time and O(1) auxiliary space excluding the output

---

## Day 59 — Maximum Product Subarray

Added `maximum_product_subarray.py`.

Topics:

- Tracking both maximum and minimum products
- Handling negative values by swapping the active extrema
- Resetting the running product at zero
- O(n) time and O(1) auxiliary space
