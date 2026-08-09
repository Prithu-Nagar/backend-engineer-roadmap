from multiprocessing import Process


def square(number: int) -> None:
    print(f"{number} squared = {number * number}")


def main() -> None:
    processes = []

    for number in range(1, 5):
        process = Process(target=square, args=(number,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()