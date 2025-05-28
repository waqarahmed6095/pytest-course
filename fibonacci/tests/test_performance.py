import pytest

from fibonacci.conftest import track_performance
from fibonacci.dynamic import fibonacci_dynamic_v2


@pytest.mark.performance
@track_performance
def test_performance():

    fibonacci_dynamic_v2(1000)
