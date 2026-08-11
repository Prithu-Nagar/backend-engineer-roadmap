"""
Day 11
AsyncIO Basics
"""

import asyncio


async def fetch_data(name, delay):
    print(f"Starting {name}")
    await asyncio.sleep(delay)
    print(f"Finished {name}")
    return f"{name} result"


async def main():
    results = await asyncio.gather(
        fetch_data("Task 1", 2),
        fetch_data("Task 2", 1),
    )

    print(results)


if __name__ == "__main__":
    asyncio.run(main())