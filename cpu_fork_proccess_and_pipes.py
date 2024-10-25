import os
import sys
import time

from utils import is_needed, clear_result_dir, check_last_saved_answer_in_files


def main():
    start = 1_000_000_000
    end = 17_000_000_000
    processes = 16
    step = (end - start) // processes

    pipes = []
    pids = []

    start_time = time.time()
    clear_result_dir()

    for i in range(processes):
        # Create a pipe for each child
        read_end, write_end = os.pipe()
        pid = os.fork()
        if pid == 0:
            # Child process
            os.close(read_end)  # Close the read end in child
            child_start = start + i * step + 1
            child_end = start + (i + 1) * step

            for n in range(child_start - child_start % 240 + 1, child_end, 240):
                if is_needed(n):
                    found_number = n.to_bytes(8, byteorder="little", signed=False)
                    os.write(write_end, found_number)
            os.close(write_end)
            os._exit(0)  # Exit child process
        else:
            # Parent process
            os.close(write_end)  # Close the write end in parent
            pipes.append(read_end)
            pids.append(pid)

    # Parent process: Read from pipes
    output_file = open("needed/needed_numbers_fork_and_pipe.txt", "a")

    for read_end in pipes:
        while True:
            data = os.read(read_end, 8)
            if not data:
                break
            received_number = int.from_bytes(data, byteorder="little", signed=False)
            print(f"Received: {received_number}")
            output_file.write(f"{received_number}\n")
        os.close(read_end)

    # Wait for all child processes to finish
    for pid in pids:
        os.waitpid(pid, 0)

    output_file.close()

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Time: {elapsed} seconds")

    is_correct = check_last_saved_answer_in_files()
    if is_correct:
        print("All files are correct")
    else:
        print("Some files are incorrect")

    input("Press Enter to exit...")


if __name__ == "__main__":
    if os.name != 'posix':
        sys.exit("Ошибка: этот скрипт должен запускаться на Unix-подобной операционной системе.")
    main()
