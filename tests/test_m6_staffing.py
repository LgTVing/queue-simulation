"""
tests/test_m6_staffing.py: Kiem thu toi uu theo gio cong ca (M6):
1. Moi do phu liet ke co tong = gio cong va x tao ra dung do phu do
2. Lich 48 (phu dung bang MILP) xuat hien trong tap do phu W = 48
3. Lich Erlang-A 44 la do phu duy nhat W = 44 khi moi gio >= SIPP Erlang-A
"""

import numpy as np
import b_shifts
import h_staffing as hs

SIPP_A = [4, 5, 6, 5, 5, 5, 5, 5, 4]


def test_coverage_vectors_consistent():
    A, c, _, _ = b_shifts.create_shifts("B", (3, 5))
    covs = hs.coverage_vectors(48, [3] * 9)
    assert len(covs) > 0
    for cov, x in covs.items():
        assert sum(cov) == 48
        assert int(np.dot(x, c)) == 48
        assert tuple(int(v) for v in A @ np.array(x)) == cov


def test_lich_48_in_search_space():
    rob = (4, 6, 6, 6, 5, 5, 6, 5, 5)
    assert rob in hs.coverage_vectors(48, SIPP_A)
    milp = b_shifts.solve_shift_scheduling(list(rob), exact_coverage=True)
    assert milp["success"] and milp["total_work_hours"] == 48


def test_w44_only_erlang_a():
    assert list(hs.coverage_vectors(44, SIPP_A)) == [tuple(SIPP_A)]
