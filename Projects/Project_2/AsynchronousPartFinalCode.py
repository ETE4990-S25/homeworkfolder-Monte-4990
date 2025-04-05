import asyncio
import time
# given code from lab 
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



async def check_prime(n):
    if is_prime(n):
        return n
    return None

async def async_prime():
    start = time.time()
    highest = 0
    n = 0
    # 180 seconds
    while time.time() - start < 180:
        result = await check_prime(n)
        if result and result > highest:
            highest = result
        n += 1
    print("Asynchronous method highest prime number after 3 minutes:", highest)
    fib_result = fibonacci(highest)
    fact_result = factorial(highest)
    print("Fibonacci of highest prime calculated.")
    print("Factorial of highest prime calculated.")



if __name__ == "__main__":
    asyncio.run(async_prime())
