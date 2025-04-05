import threading
import time

# thread lock method
max_prime = 0
lock = threading.Lock()

# given code from lab

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


# 3 minutes long to search using threads. n+2 is added constantly and gets sent to max_prime
def thread_worker(start):
    global max_prime
    n = start
    while time.time() - start_time < 180:
        if is_prime(n):
            with lock:
                if n > max_prime:
                    max_prime = n
        n += 2

def threaded_prime():
    global start_time
    start_time = time.time()
    
    t1 = threading.Thread(target=thread_worker, args=(1,))
    t2 = threading.Thread(target=thread_worker, args=(2,))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    fib_result = fibonacci(max_prime)
    fact_result = factorial(max_prime)

    print("Threaded (2 threads) highest prime:", max_prime)
    print("Fibonacci of highest prime calculated.")
    print("Factorial of highest prime calculated.")

if __name__ == "__main__":
    threaded_prime()