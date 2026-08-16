# Hashing

Hashing is a technique used to provide efficient average-case lookup, insertion, and membership checking.

Python provides built-in hash-based data structures such as:

- `dict`
- `set`

Hashing is one of the most important patterns for backend and interview problems because it can reduce lookup operations from O(n) to O(1) average time.

---

## Core Concepts

### Frequency Maps

A frequency map stores how many times each value occurs.

Example:

```python
values = [1, 2, 2, 3, 3, 3]

frequency = {
    1: 1,
    2: 2,
    3: 3,
}
Python dictionaries are commonly used to implement frequency maps.

Typical operations:

frequency[value] = frequency.get(value, 0) + 1

Average lookup and insertion:

Time: O(1)
Sets

A set stores unique values.

Example:

values = {1, 2, 3}

Sets are useful for:

Duplicate detection
Membership testing
Removing duplicates
Tracking visited values
Detecting consecutive sequences

Average membership lookup:

value in values

Time:

Average: O(1)
Hash Collision Intuition

A hash function maps a value to a hash value that is used to determine where the value should be stored.

Conceptually:

Value
  |
  v
Hash Function
  |
  v
Hash Value
  |
  v
Storage Location

Different values can sometimes produce the same hash location.

This is called a hash collision.

Hash-based data structures use internal mechanisms to handle collisions while maintaining efficient average-case operations.

Common Hashing Patterns
Frequency Counting
Input
  |
  v
Dictionary
  |
  v
Count occurrences

Useful for:

Character frequencies
Duplicate detection
Counting numbers
Anagram problems
Membership Checking
Input
  |
  v
Set
  |
  v
O(1) average lookup

Useful for:

Duplicate detection
Visited elements
Existence checks
Prefix Sum + Hash Map

A hash map can store previously seen prefix sums.

For example:

current_sum - previous_sum = target

Therefore:

previous_sum = current_sum - target

This pattern is useful for problems such as:

Subarray Sum Equals K
Prefix-sum based counting problems
LeetCode Problems
Group Anagrams

File: group_anagrams.py

Pattern:

Frequency map
Hashable representation of character counts
Longest Consecutive Sequence

File: longest_consecutive_sequence.py

Pattern:

Set membership
Detect sequence starting points
Avoid unnecessary repeated traversal
Subarray Sum Equals K

File: subarray_sum_equals_k.py

Pattern:

Prefix sum
Frequency map
Count previously observed prefix sums