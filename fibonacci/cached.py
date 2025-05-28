from functools import lru_cache

cache = {}


def fibonacci_cached(n: int) -> int:
    if n in cache:
        return cache[n]
    if n <= 0:
        return 0
    if n == 1:
        return 1
    cache[n] = fibonacci_cached(n - 1) + fibonacci_cached(n - 2)
    return cache[n]


@lru_cache(maxsize=256)
def fibonacci_lru_cache(n: int) -> int:
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_lru_cache(n - 1) + fibonacci_lru_cache(n - 2)
