"""
tests/test_sim.py: Kiem thu tu dong he thong mo phong SimPy:
1. Kiem tra dinh luat Little ve hieu suat quay rho = lam * E[S] / c
2. Kiem tra tinh tai lap tuyet doi khi dung cung seed (CRN)
3. Kiem tra tinh don dieu cua so quay (them quay khong lam xau di SL)
4. Kiem tra cong thuc Pollaczek-Khinchine cho hang doi M/G/1
5. Kiem tra hieu suat co khach bo ve (Erlang-A): rho = lam * (1 - p_ab) * E[S] / c
"""

import numpy as np
import pytest
from common import Model, exp_service, lognorm_service
import c_sim as cs

def test_utilization_matches_little():
    """Kiem tra hieu suat quay khop dinh luat Little (bat loi rho Tuan 2)."""
    lam, ms, c = 1.5, 3.0, 6
    m = Model([lam], exp_service(ms), theta=0.0, p_vip=0.0, hour_len=8000.0)
    rep_res = cs.run_reps(m, [c], n_reps=20, run_time=5000.0, warm_up=500.0, seed_base=101)
    util_sim = rep_res["hourly"][0]["util_mean"]
    expected_rho = lam * ms / c  # 0.75
    assert util_sim == pytest.approx(expected_rho, abs=0.02)

def test_same_seed_same_result():
    """Kiem tra tinh tai lap hoan toan cua CRN khi dung cung seed."""
    lam = 1.5
    m = Model([lam], exp_service(3.0), theta=0.0, p_vip=0.0, hour_len=1000.0)
    df1 = cs.simulate(m, [6], run_time=1000.0, seed=777)
    df2 = cs.simulate(m, [6], run_time=1000.0, seed=777)
    assert len(df1) == len(df2)
    assert np.allclose(df1["wait"].values, df2["wait"].values)
    assert np.array_equal(df1["served"].values, df2["served"].values)

def test_more_servers_not_worse():
    """Kiem tra tang so quay thi SL khong giam (tinh don dieu)."""
    lam = 1.5
    m = Model([lam], exp_service(3.0), theta=0.0, p_vip=0.0, hour_len=2000.0)
    res_c5 = cs.run_reps(m, [5], n_reps=10, run_time=2000.0, seed_base=42)
    res_c7 = cs.run_reps(m, [7], n_reps=10, run_time=2000.0, seed_base=42)
    assert res_c7["sl_mean"] > res_c5["sl_mean"]

def test_mg1_pollaczek_khinchine():
    """Kiem tra M/G/1 Pollaczek-Khinchine chinh xac voi phuc vu Lognormal."""
    lam = 0.25
    es = 3.0
    cv = 1.5
    cs2 = cv ** 2
    rho = lam * es
    wq_pk_exact = rho * es * (1.0 + cs2) / (2.0 * (1.0 - rho))  # 14.625 phut
    
    m = Model([lam], lognorm_service(es, cv), theta=0.0, p_vip=0.0, hour_len=8000.0)
    res = cs.run_reps(m, [1], n_reps=40, run_time=8000.0, warm_up=500.0, seed_base=123)
    wq_sim = res["wq_mean"]
    ci_half = res["wq_ci_half"]
    
    # Ly thuyet 14.625 phai nam trong khoang tin cay 95%
    assert abs(wq_sim - wq_pk_exact) <= ci_half or abs(wq_sim - wq_pk_exact) / wq_pk_exact < 0.10

def test_erlang_a_utilization():
    """Kiem tra hieu suat co khach bo ve: rho = lam * (1 - p_ab) * E[S] / c."""
    lam = 2.0
    es = 3.0
    th = 0.1
    c = 6
    m = Model([lam], exp_service(es), theta=th, p_vip=0.0, hour_len=8000.0)
    res = cs.run_reps(m, [c], n_reps=20, run_time=5000.0, warm_up=500.0, seed_base=202)
    
    util_sim = res["hourly"][0]["util_mean"]
    p_ab_sim = res["p_ab_mean"]
    expected_rho = lam * (1.0 - p_ab_sim) * es / c
    assert util_sim == pytest.approx(expected_rho, abs=0.02)
