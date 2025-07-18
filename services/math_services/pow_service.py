def compute_pow(base: float, exponent: float) -> float | str:
    x = base ** exponent
    if x > 10**200:
        return str(x)
    else:
        return x
