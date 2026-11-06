# conftest.py
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: test chay lau (smoke test pipeline); bo qua bang -m 'not slow'")


@pytest.fixture(autouse=True)
def _clear_run_cache():
    """O1: moi test bat dau voi bo nho dem run_reps rong de cac test doc lap nhau."""
    import c_sim
    c_sim.clear_run_cache()
    yield
