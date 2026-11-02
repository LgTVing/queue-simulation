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


V5_CHECKS = (cc.check_shift_staffing, cc.check_p_day, cc.check_surge, cc.check_forecast, cc.check_weibull,
             cc.check_half_hour, cc.check_cv_sensitivity, cc.check_decision_table, cc.check_class_sl)


def _v5_errors(md: str):
    ck = cc.TableChecker(md)
    for f in V5_CHECKS:
        f(ck)
    return ck.errors


@pytest.mark.skipif(not os.path.exists(os.path.join(cc.RESULTS, "chinh_sach_tang_quay.csv")),
                    reason="chua co ket qua M6-M8")
@pytest.mark.parametrize("old, new, prefix", [
    ("| 1 | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | 4 ca 8h + 4 ca 4h | 0.9579 ± 0.0017 | 0.9327",
     "| 1 | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | 4 ca 8h + 4 ca 4h | 0.9579 ± 0.0017 | 0.9337", "7.9"),
    ("(Lịch 48) | 4 ca 8h + 4 ca 4h | 0.9579", "(Lịch 48) | 4 ca 8h + 4 ca 4h | 0.9589", "7.9 linh hoat"),
    ("94.2% [93.0%, 95.1%]", "94.2% [93.0%, 95.9%]", "7.10"),
    ("| 0.8997 (11h-12h) | 1 |", "| 0.8997 (11h-12h) | 0 |", "4.6"),
    ("| 46.17 | 0.9549 |", "| 46.17 | 0.9559 |", "7.11"),
    ("| 0.9193 | 0.9128 | 0.8748 |", "| 0.9193 | 0.9128 | 0.8848 |", "7.11"),
    ("| **Lịch 48 cố định** | 48.00 | 94.0%", "| **Lịch 48 cố định** | 48.00 | 95.0%", "1 M8"),
    ("**Trên 4 ngày test: RMSE $63.9$ khách.**", "**Trên 4 ngày test: RMSE $53.9$ khách.**", "4.4"),
    ("| -1666.9 | **3337.8** |", "| -1666.9 | **3327.8** |", "7.12"),
    ("| 8h-9h | 0.8667 | 1.1133 |", "| 8h-9h | 0.8667 | 1.1233 |", "7.13"),
    ("| 0.9068 (16h-17h) | 0.9398 | 0.9241 |", "| 0.9068 (16h-17h) | 0.9398 | 0.9341 |", "7.13"),
    ("**29.0% [27.8%, 30.1%]**<br>bootstrap [25.4%, 32.3%]", "**29.0% [27.8%, 30.1%]**<br>bootstrap [25.4%, 33.3%]", "4.2"),
    (r"45.2\%]$)<br>bootstrap [40.0%, 47.5%]", r"45.2\%]$)<br>bootstrap [41.0%, 47.5%]", "1 boot"),
])
def test_v5_sections_detect_error(old, new, prefix):
    """D4: tong_hop.md muc 1, 4.2, 4.4, 7.9-7.13 khop CSV; sua mot so thi bao dung mot loi o dung muc."""
    md = open(os.path.join(BASE_DIR, "tong_hop.md"), encoding="utf-8").read()
    assert _v5_errors(md) == []
    assert md.count(old) == 1
    errors = _v5_errors(md.replace(old, new))
    assert len(errors) == 1 and errors[0].startswith(prefix)
