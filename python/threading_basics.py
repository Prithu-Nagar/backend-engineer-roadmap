"""
Python Threading Basics

Demonstrates creating threads, starting threads,
and waiting for threads using join().
"""

import threading


def task(name):
    print(f"Running {name}")


def main():
    thread1 = threading.Thread(
        target=task,
        args=("Task 1",),
    )

    thread2 = threading.Thread(
        target=task,
        args=("Task 2",),
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("All tasks completed.")


if __name__ == "__main__":
    main()