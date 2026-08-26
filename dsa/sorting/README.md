# Sorting

This directory contains comparison-based sorting algorithms and sorting-oriented
LeetCode problems covered in the Backend Engineer Roadmap.

## Day 26 — Sorting

Topics:

- Merge sort
- Quicksort
- Divide-and-conquer partitioning
- Stable vs unstable sorting
- Best, average, and worst-case complexity
- Choosing a sorting strategy for interview problems

Implementations:

- `merge_sort.py`
- `quick_sort.py`
- `sort_array.py` — LeetCode: Sort an Array

## Stability

A stable sorting algorithm preserves the relative order of equal elements. Merge
sort is naturally stable when equal values are merged from the left side first.
The quicksort implementation here does not provide a stability guarantee.

## Complexity Comparison

| Algorithm | Best | Average | Worst | Stable |
|---|---:|---:|---:|---|
| Merge Sort | O(N log N) | O(N log N) | O(N log N) | Yes |
| Quick Sort | O(N log N) | O(N log N) | O(N²) | No |
