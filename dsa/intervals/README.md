# Intervals

Interval problems involve ranges represented as:

```text
[start, end]
```

The most common interview pattern is:

1. Sort intervals by their start time.
2. Compare the current interval with the previous merged interval.
3. Merge overlapping intervals.
4. Otherwise, start a new interval.

## Core Pattern

Given:

```text
[[1,3], [2,6], [8,10], [9,12]]
```

Sort by start:

```text
[1,3]
[2,6]
[8,10]
[9,12]
```

Merge overlapping ranges:

```text
[1,6]
[8,12]
```

Result:

```text
[[1,6], [8,12]]
```

## Important Conditions

Two intervals overlap when:

```text
current_start <= previous_end
```

For example:

```text
[1,5]
[4,8]
```

Since:

```text
4 <= 5
```

they overlap.

The merged interval becomes:

```text
[1,8]
```

## General Merge Algorithm

```text
sort intervals by start

result = []

for interval in intervals:

    if result is empty:
        add interval

    elif interval.start <= result[-1].end:
        merge intervals

    else:
        add interval
```

## Complexity

For `n` intervals:

Sorting:

```text
O(n log n)
```

Linear merge pass:

```text
O(n)
```

Overall:

```text
Time: O(n log n)
Space: O(n)
```

The additional space may be considered `O(1)` apart from the output depending on the problem's space-complexity convention.
