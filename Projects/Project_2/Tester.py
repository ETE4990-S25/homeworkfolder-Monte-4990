from multiprocessing import Pool, cpu_count
import time
from itertools import count

import time

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def worker(n):
    if is_prime(n):
        return n
    return None

def multiprocessing_prime():
    start_time = time.time()
    timeout = 180  # seconds
    max_prime = 0

    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap(worker, count(0)):
            if result and result > max_prime:
                max_prime = result
            if time.time() - start_time > timeout:
                break

    print("Multiprocessing highest prime:", max_prime)

if __name__ == "__main__":
    multiprocessing_prime()