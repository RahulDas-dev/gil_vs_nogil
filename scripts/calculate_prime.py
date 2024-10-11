from concurrent.futures import ThreadPoolExecutor
import time


def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


def count_primes(start: int, end: int):
    count = 0
    for number in range(start, end + 1):
        if is_prime(number):
            count += 1
    return count


def single_thread(numbers):
    count = count_primes(2, numbers)
    return count


def multi_thread(numbers: int, num_threads: int):
    chunk_size = numbers // num_threads
    results, features = [], []
    start = 2
    with ThreadPoolExecutor() as executor:
        for i in range(num_threads):
            end = start + chunk_size if i < num_threads - 1 else numbers
            future = executor.submit(count_primes, start, end)
            features.append(future)
            start = end + 1

        for future in features:
            results.append(future.result())
    return sum(results)


# Banchmarking
if __name__ == "__main__":
    numbers = 5000000
    print("Benchmaking single-Threded")
    start_time = time.perf_counter()
    prime_count = single_thread(numbers)
    end_time = time.perf_counter()
    print(f"Found {prime_count} primes in {end_time - start_time} seconds")

    print("Benchmaking multi-Threded thread count 4")
    start_time = time.perf_counter()
    prime_count = multi_thread(numbers, 4)
    end_time = time.perf_counter()
    print(f"Found {prime_count} primes in {end_time - start_time} seconds")

    print("Benchmaking multi-Threded thread count 8")
    start_time = time.perf_counter()
    prime_count = multi_thread(numbers, 8)
    end_time = time.perf_counter()
    print(f"Found {prime_count} primes in {end_time - start_time} seconds")
