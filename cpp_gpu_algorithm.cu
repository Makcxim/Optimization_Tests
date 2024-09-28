#include <iostream>
#include <fstream>
#include <cmath>
#include <cuda.h>
#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <chrono>

// __device__ функция для проверки простоты числа
__device__ bool is_prime(uint64_t n) {
    if (n < 2) return false;
    for (uint64_t i = 2; i <= sqrt((double)n); ++i) {
        if (n % i == 0) return false;
    }
    return true;
}

// __device__ функция для проверки, имеет ли число ровно 5 делителей
__device__ bool is_needed(uint64_t n) {
    double sqrt_root = pow((double)n, 1.0 / 4.0);
    if (floor(sqrt_root) == sqrt_root && is_prime((uint64_t)sqrt_root)) {
        return true;
    }
    return false;
}

// __global__ функция-ядро для поиска чисел и записи результатов
__global__ void find_primes(uint64_t adjusted_start, uint64_t total_steps, uint64_t *results, uint64_t *result_count) {
    uint64_t idx = blockIdx.x * blockDim.x + threadIdx.x;
    uint64_t stride = gridDim.x * blockDim.x;

    for (uint64_t i = idx; i < total_steps; i += stride) {
        uint64_t n = adjusted_start + i * 240;
        if (is_needed(n)) {
            // Атомарное увеличение счетчика результатов
            uint64_t index = atomicAdd(result_count, 1);
            if (index < 500) { // Проверка на переполнение массива
                results[index] = n;
            }
        }
    }
}

int main() {
    uint64_t start = 1'000'000'000;
    uint64_t end = 17'000'000'000;

    // Оценка максимального числа результатов
    const int max_results = 500;

    uint64_t *d_results;
    uint64_t *d_result_count;

    // Выравнивание начала диапазона
    uint64_t adjusted_start = start - start % 240 + 1;
    uint64_t total_steps = (end - adjusted_start) / 240;

    // Выделение памяти на устройстве
    cudaMalloc(&d_results, max_results * sizeof(uint64_t));
    cudaMalloc(&d_result_count, sizeof(uint64_t));

    // Инициализация счетчика результатов нулем
    uint64_t zero = 0;
    cudaMemcpy(d_result_count, &zero, sizeof(uint64_t), cudaMemcpyHostToDevice);

    // Настройка параметров запуска ядра
    int threads_per_block = 256;
    int blocks_per_grid = 256;

    auto start_time = std::chrono::high_resolution_clock::now();

    // Запуск ядра CUDA
    find_primes<<<blocks_per_grid, threads_per_block>>>(adjusted_start, total_steps, d_results, d_result_count);

    cudaDeviceSynchronize();

    auto end_time = std::chrono::high_resolution_clock::now();

    // Копирование результатов обратно на хост
    uint64_t result_count;
    cudaMemcpy(&result_count, d_result_count, sizeof(uint64_t), cudaMemcpyDeviceToHost);

    if (result_count > max_results) {
        result_count = max_results;
    }

    uint64_t *h_results = new uint64_t[result_count];
    cudaMemcpy(h_results, d_results, result_count * sizeof(uint64_t), cudaMemcpyDeviceToHost);

    // Запись результатов в файл
    std::ofstream file("needed_cuda.txt", std::ios::app);
    for (uint64_t i = 0; i < result_count; ++i) {
        std::cout << h_results[i] << std::endl;
        file << h_results[i] << "\n";
    }
    file.close();

    std::chrono::duration<double> elapsed = end_time - start_time;
    std::cout << "Time: " << elapsed.count() << " seconds" << std::endl;

    // Очистка памяти
    cudaFree(d_results);
    cudaFree(d_result_count);
    delete[] h_results;

    // Ожидание перед закрытием программы
    std::cout << "Press Enter to exit..." << std::endl;
    std::cin.get();

    return 0;
}
