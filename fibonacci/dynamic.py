def fibonacci_dynamic(n: int) -> int:
    fib_list = [0, 1]

    for i in range(1, n + 1):
        fib_list.append(fib_list[i] + fib_list[i - 1])
    return fib_list[n]


def fibonacci_dynamic_V2(n: int) -> int:
    fib_1 = 0
    fib_2 = 1

    for i in range(1, n + 1):
        fib = fib_1 + fib_2
        fib_1 = fib_2
        fib_2 = fib
    return fib_1
