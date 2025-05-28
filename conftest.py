from datetime import datetime, timedelta
from typing import Callable

import pytest


@pytest.fixture
def time_tracker():
    tick = datetime.now()
    yield
    tock = datetime.now()
    diff = tock - tick
    print(f"\n run time: {diff.total_seconds() } seconds")


def track_performance(method: Callable, runtime_limit=timedelta(seconds=2)):
    def run_function_and_validate_runtime(*args, **kwargs):
        tick = datetime.now()
        result = method(*args, **kwargs)
        tock = datetime.now()
        runtime = tock - tick
        print(f"\n run time: {runtime.total_seconds() } seconds")
        if runtime > runtime_limit:
            raise PerformanceException(
                f"Test took {runtime.total_seconds() } seconds to run, which is longer than the limit of {runtime_limit.total_seconds() } seconds"
            )
        return result

    return run_function_and_validate_runtime
