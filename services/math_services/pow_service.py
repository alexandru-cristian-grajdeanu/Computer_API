from exceptions.PowTooLargeError import PowTooLargeError
from functools import lru_cache

from logger import logger


@lru_cache(maxsize=64)
def compute_pow(base: float, exponent: float) -> float | str:
    logger.info(f"[Cache MISS] compute_fibonacci({base}, {exponent})")
    if base == 0 and exponent <= 0:
        raise ValueError("0 cannot be raised to 0 or a negative exponent.")

    if base < 0 and not exponent.is_integer():
        raise ValueError("Negative base with fractional exponent is a complex number.")

    if abs(int(base)) > 1e154 or abs(int(exponent)) > 1e10:
        raise PowTooLargeError("Base or exponent too large to compute safely.")
    try:
        x = base ** exponent
    except OverflowError:
        raise PowTooLargeError("Overflow during power computation.")

    return str(x) if abs(x) > 10 ** 200 else x
