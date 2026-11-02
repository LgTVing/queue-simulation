"""
tests/test_v51_fixes.py: Kiem thu cac ban sua V5.1 (docs/KE_HOACH_V5_1.md):
1. F10: optimize_schedule bao "feasible"; lich khong dat khi qua tai va c_cap nho
2. F10: sipp_schedule canh bao khi roi vao nhanh du phong
"""

import numpy as np
import pytest

from common import Model, exp_service
import b_theory as th
import c_sim as cs


def test_optimize_reports_infeasible():
    """F10: lambda 2/phut, E[S] 3 phut (a = 6) ma c_cap = 2 -> khong the dat SLA."""
    m = Model(rates=[2.0, 2.0], service=exp_service(3.0), theta=0.1, p_vip=0.0, mean_svc=3.0)
    res = cs.optimize_schedule(m, initial_schedule=[1, 1], n_reps=5, c_cap=2, seed_base=1)
    assert res["feasible"] is False
    assert max(res["schedule"]) <= 2


def test_optimize_reports_feasible():
    m = Model(rates=[0.2, 0.2], service=exp_service(3.0), theta=0.1, p_vip=0.0, mean_svc=3.0)
    res = cs.optimize_schedule(m, initial_schedule=[4, 4], n_reps=10, seed_base=1)
    assert res["feasible"] is True
    assert cs.is_schedule_feasible(res["eval"])[0]


def test_sipp_fallback_warns():
    # Muc tieu > 1 khong bao gio dat -> nhanh du phong c_start + 5 (c_start = floor(a) + 1 = 6)
    with pytest.warns(UserWarning, match="sipp_schedule"):
        sched = th.sipp_schedule([5.0], 1.0, 0.0, target=1.01, use_erlang_a=False)
    assert sched == [11]
