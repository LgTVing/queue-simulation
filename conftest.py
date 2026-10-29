# conftest.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: test chay lau (smoke test pipeline); bo qua bang -m 'not slow'")
