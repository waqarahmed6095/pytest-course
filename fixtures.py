from datetime import datetime
import pytest


@pytest.fixture
def time_tracker():
    tick = datetime.now()
    yield
    tock = datetime.now()
    diff = tock - tick
    print(f"\n run time: {diff.total_seconds() } seconds")



