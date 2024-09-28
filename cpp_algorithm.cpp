#include <iostream>
#include <fstream>
#include <cmath>
#include <thread>
#include <vector>
#include <mutex>
#include <sys/stat.h>
#include <string>

std::mutex mtx; // Для синхронизации файловых операций

// Проверяет, является ли число простым
bool is_prime(uint64_t n) {
    if (n < 2) return false;
    for (uint64_t i = 2; i <= std::sqrt(n); ++i) {
        if (n % i == 0) return false;
    }
    return true;
}

// Проверяет, имеет ли число ровно 5 делителей
bool is_needed(uint64_t n) {
    double sqrt_root = std::pow(n, 1.0 / 4.0);
    if (std::floor(sqrt_root) == sqrt_root && is_prime(static_cast<uint64_t>(sqrt_root))) {
        return true;
    }
    return false;
}

// Функция для поиска чисел в заданном диапазоне и записи в файл
void find_primes(uint64_t start, uint64_t end, int thread_number) {
    std::string folder = "needed";
    std::ofstream file("needed/needed_" + std::to_string(thread_number) + ".txt", std::ios::app);

    for (uint64_t i = start - start % 240 + 1; i < end; i=i+240) {
        if (is_needed(i)) {
            std::cout << i << std::endl;
            std::lock_guard<std::mutex> lock(mtx); // Синхронизация записи в файл
            file << i << "\n";
        }
    }
    file.close();
}

// Главная функция для запуска потоков
int main() {
    uint64_t start = 1'000'000'000;
    uint64_t end = 17'000'000'000;
    int threads = 16;
    uint64_t step = (end - start) / threads;

    std::vector<std::thread> thread_list;
    auto start_time = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < threads; ++i) {
        thread_list.emplace_back(find_primes, start + i * step + 1, start + (i + 1) * step, i);
    }

    // Ожидание завершения всех потоков
    for (auto& th : thread_list) {
        th.join();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;
    std::cout << "Time: " << elapsed.count() << " seconds" << std::endl;

    // do not close programm
    std::cout << "Press Enter to exit..." << std::endl;
    std::cin.get();

    return 0;
}