"""
Day 25 — Debugging, Profiling Basics & Reading Tracebacks

The examples demonstrate a practical workflow for locating failures and
measuring slow code before making a performance change.
"""

from __future__ import annotations

import cProfile
import pstats
import timeit


def parse_count(value: str) -> int:
    """Convert a string to an integer and let invalid input fail clearly."""

    return int(value)


def sum_with_loop(values: list[int]) -> int:
    total = 0
    for value in values:
        total += value
    return total


def sum_with_builtin(values: list[int]) -> int:
    return sum(values)


def benchmark(values: list[int]) -> tuple[float, float]:
    """Compare two implementations using timeit."""

    loop_time = timeit.timeit(lambda: sum_with_loop(values), number=1000)
    builtin_time = timeit.timeit(lambda: sum_with_builtin(values), number=1000)
    return loop_time, builtin_time


def profile_function(values: list[int]) -> pstats.Stats:
    """Profile a function and return statistics for inspection."""

    profiler = cProfile.Profile()
    profiler.enable()
    sum_with_loop(values)
    profiler.disable()
    return pstats.Stats(profiler).sort_stats("cumulative")


if __name__ == "__main__":
    sample = list(range(10_000))
    print("Benchmark:", benchmark(sample))
    profile_function(sample).print_stats(5)
