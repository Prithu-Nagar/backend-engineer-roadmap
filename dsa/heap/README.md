# Heap

This directory contains Heap-based LeetCode solutions implemented throughout the Backend Engineer Roadmap.

The focus is on understanding priority queues, min-heaps, max-heaps, and their applications in common interview problems.

---

## Problems

- Kth Largest Element in an Array
- Top K Frequent Elements
- Last Stone Weight
- K Closest Points to Origin
- Merge K Sorted Lists
- Find Median from Data Stream

---

## Concepts Covered

- Min Heap
- Max Heap
- Python `heapq`
- Heap construction
- Heap insertion and removal
- Maintaining top K elements
- Heap-based selection
- Two-heap approach for median finding

---

## Complexity

Heap insertion:

- Time: O(log n)

Heap removal:

- Time: O(log n)

Heap construction:

- Time: O(n)

Accessing the smallest element:

- Time: O(1)

Maintaining K elements:

- Time: O(n log k)

---

## Repository Files

- `kth_largest_element.py`
- `top_k_frequent_elements.py`
- `last_stone_weight.py`
- `k_closest_points_to_origin.py`
- `merge_k_sorted_lists.py`
- `find_median_from_data_stream.py`

---

## Day 38 — Heap + Greedy

Day 38 combines heap-based priority selection with greedy decisions.

Problems:

- Task Scheduler
- Reorganize String

Concepts:

- Max-heap simulation with `heapq`
- Frequency counting
- Cooldown scheduling
- Greedy placement
- Priority-based selection

Repository files:

- `task_scheduler.py`
- `reorganize_string.py`

---

## Day 48 — Greedy + Heap Review

Day 48 revisits greedy decision-making supported by heaps.

Problems:

- IPO
- Furthest Building You Can Reach
- Maximum Performance of a Team

The review emphasizes sorting by the constraint that becomes active, using a
heap to keep the best currently available choices, and proving why replacing
the weakest selected option preserves the optimal candidate set.

Repository files:

- `ipo.py`
- `furthest_building_you_can_reach.py`
- `maximum_performance_of_a_team.py`

---

## Day 56 — Heap + Greedy

Day 56 extends heap usage into greedy decision-making and priority-based
selection.

Problems:

- Kth Smallest Element in a Sorted Matrix
- Meeting Rooms II
- Minimum Number of Refueling Stops

Concepts:

- Min-heap over sorted row candidates
- Greedy interval allocation
- Tracking active meeting end times
- Max-heap selection of previously reachable fuel
- Delaying a greedy commitment until additional information is available

Repository files:

- `kth_smallest_element_in_sorted_matrix.py`
- `meeting_rooms_ii.py`
- `minimum_number_of_refueling_stops.py`
