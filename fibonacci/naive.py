def fibonacci_naive(n: int) -> int:
    """
    Calculate the nth Fibonacci number using a naive recursive approach.

    Args:
        n (int): The position in the Fibonacci sequence.

    Returns:
        int: The nth Fibonacci number.
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


print(fibonacci_naive(10))
