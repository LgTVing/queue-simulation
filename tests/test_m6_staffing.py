"""
tests/test_m6_staffing.py: Kiem thu toi uu theo gio cong ca (M6):
1. Moi do phu liet ke co tong = gio cong va x tao ra dung do phu do
2. Lich 48 (phu dung bang MILP) xuat hien trong tap do phu W = 48
3. Lich Erlang-A 44 la do phu duy nhat W = 44 khi moi gio >= SIPP Erlang-A
4. Nghi trua linh hoat 9h-16h: khong gian chua nghi 11h-14h, dem ca dung
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


def test_flexible_lunch_space():
    """Nghi trua 9h-16h: W = 44 van chi co lich Erlang-A; W = 48 chua moi do phu cua nghi 11h-14h."""
    flex = (1, 7)
    assert list(hs.coverage_vectors(44, SIPP_A, flex)) == [tuple(SIPP_A)]
    assert set(hs.coverage_vectors(48, SIPP_A)) <= set(hs.coverage_vectors(48, SIPP_A, flex))
    for cov, x in hs.coverage_vectors(48, SIPP_A, flex).items():
        n8, n4 = hs.shift_counts(x, flex)
        assert 8 * n8 + 4 * n4 == 48


# ----------------------------------------------------------------------------- M7
from common import Model, empirical_service  # noqa: E402
from stats_utils import wilson_ci  # noqa: E402
import c_sim as cs  # noqa: E402


def _small_model():
    return Model(rates=[1.2, 1.6, 1.0], service=empirical_service(np.random.default_rng(1).gamma(1.1, 2.7, 500)),
                 theta=0.1, p_vip=0.35)


def test_p_day_matches_definition():
    """M7: P = ti le lan lap co SL ngay >= 90%, Wilson tinh tren so lan lap; ket qua dem lai giong het."""
    m, sched = _small_model(), [4, 5, 4]
    r = hs.p_day(m, sched, cv_day=0.14, n_reps=40, seed=123)
    ref = cs.run_reps(m, sched, n_reps=40, seed_base=123, day_cv=0.14, keep_reps=True)
    k = int(np.sum(np.asarray(ref["rep_sl_day"]) >= 0.90))
    p, lo, hi, _ = wilson_ci(k, 40)
    assert (r["p"], r["low"], r["high"]) == (p, lo, hi)
    assert hs.p_day(m, sched, cv_day=0.14, n_reps=40, seed=123) is r
