import pytest

from fibonacci.naive import fibonacci_naive


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (20, 6765),
    ],
)
def test_fibonacci_naive(n: int, expected: int):
    """
    Test the fibonacci_naive function.
    """
    res = fibonacci_naive(n=n)
    assert res == expected
