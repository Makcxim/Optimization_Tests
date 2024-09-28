import threading
import time
from multiprocessing import Process
from threading import Thread

from constants import START, STEP_THREADS, THREADS
from utils import is_needed, write_number_to_file


def get_threads_with_target(target: callable) -> list[Thread]:
    """get thread with target function"""
    threads = []
    for thread in range(THREADS):
        thread = threading.Thread(
            target=target,
            args=(START + thread * STEP_THREADS, START + (thread + 1) * STEP_THREADS, thread),
        )
        threads.append(thread)
    return threads


def calculate_cpu_threads(target: callable) -> None:
    """calculate cpu threads with target function"""
    start_time = time.time()

    threads = get_threads_with_target(target)
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Time:", time.time() - start_time)


def get_processes_with_target(target: callable) -> list[Process]:
    """Get processes with target function."""
    processes = []
    for i in range(THREADS):
        process = Process(
            target=target,
            args=(START + i * STEP_THREADS, START + (i + 1) * STEP_THREADS, i),
        )
        processes.append(process)
    return processes


def calculate_cpu_processes(target: callable) -> None:
    """Calculate CPU processes with the target function."""
    start_time = time.time()

    processes = get_processes_with_target(target)
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print("Time:", time.time() - start_time)


def find_needed_numbers(start: int, end: int, thread_number: int = 0):
    """find all numbers in range from start to end in thread_number thread"""
    for number in range(start, end):
        if is_needed(number):
            write_number_to_file(number, thread_number)
            print(number)


def find_needed_numbers_mod10(start: int, end: int, thread_number: int = 0):
    """find all numbers in range from start to end in thread_number thread that ends with 1"""
    for number in range(start, end):
        if not number % 10 == 1:
            continue

        if is_needed(number):
            write_number_to_file(number, thread_number)
            print(number)


def find_needed_numbers_mod80(start: int, end: int, thread_number: int = 0):
    """find all numbers in range from start to end in thread_number thread that ends divide by 80 with remainder = 1"""
    for number in range(start - start % 80 + 1, end, 80):
        if is_needed(number):
            write_number_to_file(number, thread_number)
            print(number)


def find_needed_numbers_mod240(start: int, end: int, thread_number: int = 0):
    """find all numbers in range from start to end in thread_number thread that ends divide by 240 with remainder = 1"""
    for number in range(start - start % 240 + 1, end, 240):
        if is_needed(number):
            write_number_to_file(number, thread_number)
            print(number)

