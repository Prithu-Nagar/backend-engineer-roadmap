# Intervals


Interval problems involve ranges represented as:


```text
[start, end]

The most common interview pattern is:

Sort intervals by their start time.
Compare the current interval with the previous merged interval.
Merge overlapping intervals.
Otherwise, start a new interval.
Core Pattern

Given:

[[1,3], [2,6], [8,10], [9,12]]

Sort by start:

[1,3]
[2,6]
[8,10]
[9,12]

Merge overlapping ranges:

[1,6]
[8,12]

Result:

[[1,6], [8,12]]
Important Conditions

Two intervals overlap when:

current_start <= previous_end

For example:

[1,5]
[4,8]

Since:

4 <= 5

they overlap.

The merged interval becomes:

[1,8]
General Merge Algorithm
sort intervals by start


result = []


for interval in intervals:


    if result is empty:
        add interval


    elif interval.start <= result[-1].end:
        merge intervals


    else:
        add interval
Complexity

For n intervals:

Sorting:

O(n log n)

Linear merge pass:

O(n)

Overall:

Time: O(n log n)
Space: O(n)

The additional space may be considered O(1) apart from the output depending on the problem's space-complexity convention.