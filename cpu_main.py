from cpu_utils import (
    calculate_cpu_processes,
    calculate_cpu_threads,
    find_needed_numbers,
    find_needed_numbers_mod10,
    find_needed_numbers_mod80,
    find_needed_numbers_mod240,
)
from utils import (
    check_last_saved_answer_in_files,
    clear_result_dir,
)


def main():
    clear_result_dir()

    """
    method:                 target:                     time:
    calculate_cpu_threads    find_needed_numbers         LAPTOP Time: 2860.514561891556
    calculate_cpu_threads    find_needed_numbers_mod10   LAPTOP Time: 991.7399344444275
    calculate_cpu_threads    find_needed_numbers_mod80   LAPTOP Time: 36.346190452575684
    calculate_cpu_threads    find_needed_numbers_mod240  LAPTOP Time: 11.737520217895508
    calculate_cpu_processes find_needed_numbers         RISKY TO RUN.. long to execute and 90 degrees on LAPTOP
    calculate_cpu_processes find_needed_numbers_mod10   RISKY TO RUN.. long to execute and 90 degrees on LAPTOP
    calculate_cpu_processes find_needed_numbers_mod80   LAPTOP Time: 4.708799839019775
    calculate_cpu_processes find_needed_numbers_mod240  LAPTOP Time: 1.5776875019073486
    """

    # calculate_cpu_threads(target=find_needed_numbers_mod240)
    calculate_cpu_processes(target=find_needed_numbers_mod240)

    is_correct = check_last_saved_answer_in_files()
    if is_correct:
        print("All files are correct")
    else:
        print("Some files are incorrect")


if __name__ == "__main__":
    main()
