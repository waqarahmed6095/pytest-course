from datetime import datetime, timedelta
from typing import Callable

import pytest


class PerformanceException(Exception):
    """
    Exception raised for performance issues.
    """

    def __init__(self, runtime: timedelta, runtime_limit: timedelta) -> None:
        self.runtime = runtime
        self.runtime_limit = runtime_limit

    def __str__(self) -> str:
        return f"Test took {self.runtime.total_seconds() } seconds to run, which is longer than the limit of {self.runtime_limit.total_seconds() } seconds"


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
            raise PerformanceException(runtime, runtime_limit)
        return result

    return run_function_and_validate_runtime
