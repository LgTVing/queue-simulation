"""
tests/test_t2_checker.py: Kiem thu doi chieu so trong bao cao, slide, README (T2):
1. Tai lieu hien tai khop CSV nguon
2. Sua sai mot so trong tung tai lieu thi checker phai bao loi o dung tep
"""

import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "tools"))
import check_consistency as cc  # noqa: E402


def _texts():
    return {k: open(p, encoding="utf-8").read() for k, p in cc.REPORT_FILES.items()}


def test_report_numbers_match():
    assert cc.check_report_numbers(_texts()) == []


@pytest.mark.parametrize("fname, old, new", [
    ("bao_cao_tong_ket.md", "0.9423 ± 0.0022", "0.9432 ± 0.0022"),
    ("slide_thuyet_trinh.md", "94.23%", "94.32%"),
    ("README.md", "0,942", "0,924"),
])
def test_report_numbers_detect_error(fname, old, new):
    texts = _texts()
    assert old in texts[fname]
    texts[fname] = texts[fname].replace(old, new)
    errors = cc.check_report_numbers(texts)
    assert errors and all(e.startswith(fname) for e in errors)
