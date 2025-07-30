import math
from exceptions.FibonacciTooLargeError import FibonacciTooLargeError
from functools import lru_cache

from logger import logger


@lru_cache(maxsize=64)
def compute_fibonacci(n: int) -> int | str:
    logger.info(f"[Cache MISS] compute_fibonacci({n})")
    if n == 0:
        return 0
    elif n == 1:
        return 1

    phi = (1 + math.sqrt(5)) / 2
    estimated_digits = int(n * math.log10(phi) - math.log10(math.sqrt(5)))

    if estimated_digits > 10000:
        raise FibonacciTooLargeError(
            f"Fibonacci number for n = {n} "
            f"would exceed {estimated_digits} digits."
        )
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    if b > 10 ** 200:
        return str(b)
    else:
        return b
