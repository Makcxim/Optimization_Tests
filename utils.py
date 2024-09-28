import math
import os

from constants import END, RESULT_DIR_NAME, RESULT_FILES_NAME, START


def is_prime(number: int) -> bool:
    """check if number is prime"""
    if number < 2:
        return False

    for divisor in range(2, int(math.pow(number, 1 / 2)) + 1):
        if number % divisor == 0:
            return False

    return True


def is_needed(number: int) -> bool:
    """check if number is 4th power of prime number"""
    sqrt = math.pow(number, 1 / 4)

    if sqrt.is_integer() and is_prime(sqrt):
        return True

    return False


def collect_numbers() -> list[int]:
    """collect all numbers from all .txt files in RESULT_DIR_NAME directory and return them as list of integers"""
    os.makedirs(RESULT_DIR_NAME, exist_ok=True)

    numbers = []
    for filename in os.listdir(RESULT_DIR_NAME):
        if filename.endswith(".txt"):
            filepath = os.path.join(RESULT_DIR_NAME, filename)
            with open(filepath, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        numbers.append(int(line))
    return numbers


def get_expected_answer() -> list[int]:
    """get expected answer for the task"""
    start_root = int(math.pow(START, 1 / 4))
    end_root = int(math.pow(END, 1 / 4))

    expected_answer = []
    for i in range(start_root - 1, end_root + 2):
        if is_prime(i):
            expected_answer.append(i**4)

    return expected_answer


def check_last_saved_answer_in_files() -> bool:
    """check needed dir and all .txt files to compare with expected results"""
    expected_answer = get_expected_answer()
    answer = collect_numbers()

    if sorted(expected_answer) != sorted(answer):
        return False

    return True


def write_number_to_file(number: int, thread_number: int):
    """write number to file"""
    with open(f"{RESULT_DIR_NAME}/{RESULT_FILES_NAME}_{thread_number}.txt", "a") as file:
        file.write(f"{number}\n")


def clear_result_dir():
    """clear RESULT_DIR_NAME directory"""
    os.makedirs(RESULT_DIR_NAME, exist_ok=True)

    for filename in os.listdir(RESULT_DIR_NAME):
        filepath = os.path.join(RESULT_DIR_NAME, filename)
        os.remove(filepath)
