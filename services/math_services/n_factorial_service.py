import math

from exceptions.FactorialTooLargeError import FactorialTooLargeError
from functools import lru_cache

from logger import logger


@lru_cache(maxsize=64)
def compute_factorial(n: int) -> int | str:
    logger.info(f"[Cache MISS] compute_factorial({n})")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    if n == 0:
        return 1

    estimated_digits = math.floor(n * math.log10(n / math.e)
                                  + math.log10(2 * math.pi * n) / 2)

    if estimated_digits > 10000:
        raise FactorialTooLargeError(
            f"Factorial result will exceed {estimated_digits} "
            f"digits, which is beyond the safe string conversion limit."
        )

    result = 1
    for i in range(2, n + 1):
        result *= i

    return str(result) if n > 170 else result
