def fibonacci_naive(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


print(fibonacci_naive(10))
