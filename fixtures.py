from datetime import datetime

import pytest

@pytest.fixture
def time_tracker():
    before_run=datetime.now()
    yield 
    after_run=datetime.now()
    difference = after_run - before_run
    print(f'\n runtime is: {difference}')
