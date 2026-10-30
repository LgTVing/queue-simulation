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


V5_CHECKS = (cc.check_shift_staffing, cc.check_p_day, cc.check_surge)


def _v5_errors(md: str):
    ck = cc.TableChecker(md)
    for f in V5_CHECKS:
        f(ck)
    return ck.errors


@pytest.mark.skipif(not os.path.exists(os.path.join(cc.RESULTS, "chinh_sach_tang_quay.csv")),
                    reason="chua co ket qua M6-M8")
@pytest.mark.parametrize("old, new, prefix", [
    ("| 0.9579 ± 0.0017 | 0.9327 (15h-16h)", "| 0.9579 ± 0.0017 | 0.9337 (15h-16h)", "7.9"),
    ("95.3% [92.3%, 97.2%]", "95.3% [92.3%, 97.9%]", "7.10"),
    ("| 46.17 | 0.9549 |", "| 46.17 | 0.9559 |", "7.11"),
    ("| **Lịch 48 cố định** | 48.00 | 94.0%", "| **Lịch 48 cố định** | 48.00 | 95.0%", "1 M8"),
])
def test_v5_sections_detect_error(old, new, prefix):
    """D4: tong_hop.md muc 7.9-7.11 va bang M8 o muc 1 khop CSV; sua mot so thi bao loi dung muc."""
    md = open(os.path.join(BASE_DIR, "tong_hop.md"), encoding="utf-8").read()
    assert _v5_errors(md) == []
    assert md.count(old) == 1
    errors = _v5_errors(md.replace(old, new))
    assert len(errors) == 1 and errors[0].startswith(prefix)
