from multiprocessing import Process, Queue, cpu_count
import time

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Idea from chatGPT to use "queue" to find highest prime number
def prime_finder(start, step, queue, timeout, proc_id):
    highest = 0 # Initialize highest prime (0) from the lab
    t0 = time.time()
    n = start
    count_checked = 0
    while time.time() - t0 < timeout:
        if is_prime(n):
            highest = n
        n += step
        count_checked += 1

    print(f"[Process {proc_id}] Checked {count_checked} numbers. Highest prime: {highest}")
    queue.put(highest)

def run_multiprocessing_prime():
    num_workers = cpu_count()
    processes = []
    queue = Queue()
    timeout = 180  


    print(f"Number of workers: {num_workers}")
    print(f"Working on finding the highest prime number, takes 3 full minutes, one moment please...")

    for i in range(num_workers):
        # Helps skip even numbers
        # Start from 3 and increment by 2 to check only odd numbers to make the process faster
        p = Process(target=prime_finder, args=(3 + i * 2, num_workers * 2, queue, timeout, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    max_prime = 0
    while not queue.empty():
        result = queue.get()
        if result > max_prime:
            max_prime = result

            # print prime number and fibonacci

    print(f"\n highest prime number: {max_prime}")
    fib_result = fibonacci(max_prime)
    fact_result = factorial(max_prime)
    print("Fibonacci of highest prime calculated.")
    print("Factorial of highest prime calculated.")

if __name__ == "__main__":
    run_multiprocessing_prime()