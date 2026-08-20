# Sliding Window


Sliding Window is a technique for processing contiguous subarrays or substrings efficiently by maintaining a moving range with two pointers.


## Core Patterns


### Fixed Window


Use when the window size is fixed at `k`.


[ a b c ] d e
    ↓
 a [ b c d ] e
Variable Window

Use when the window expands and shrinks according to a condition.

left → shrink
right → expand
Typical Complexity
Time: O(n) when both pointers move only forward.
Space: O(1) for simple numeric windows, or O(k) when using a Set/HashMap.