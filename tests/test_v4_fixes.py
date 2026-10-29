"""
tests/test_v4_fixes.py: Kiem thu cac ban sua loi V4 trong c_sim.py:
1. T1-a: Sau gio dong cua giu so quay cua gio cuoi (F1)
2. T1-b: Qua trinh den Poisson khong dong nhat dung o ranh gioi gio (F2)
3. T1-c: Blocker ton trong lich quay trong moi khung gio
4. T1-g: Hieu suat theo gio tinh theo thoi gian ban thuc te (F3)
"""

import numpy as np
import pytest
import scipy.stats as st
from common import Model, exp_service
import c_sim as cs


def busy_at(df, times):
    """So khach dang duoc phuc vu tai tung thoi diem trong times."""
    served = df[df["served"] == 1]
    s = served["start_svc"].to_numpy()[:, None]
    e = served["end_svc"].to_numpy()[:, None]
    t = np.asarray(times)[None, :]
    return ((s <= t) & (e > t)).sum(axis=0)


def test_drain_keeps_last_hour_servers():
    """T1-a: Lich [6, 2], tai qua de con hang sau 17h; sau phut 120 so quay ban <= 2."""
    m = Model([3.0, 3.0], exp_service(3.0), theta=0.0, p_vip=0.0, hour_len=60.0)
    df = cs.simulate(m, [6, 2], seed=11)
    assert (df["end_svc"] > 120.0).any()  # thuc su co xa hang sau gio dong cua
    after = df.loc[(df["served"] == 1) & (df["start_svc"] >= 120.0), "start_svc"].to_numpy()
    assert busy_at(df, after).max() <= 2

    # Hanh vi cu (all_open) mo lai 6 quay khi xa hang -> vuot qua 2
    df_old = cs.simulate(m, [6, 2], seed=11, drain_policy="all_open")
    after_old = df_old.loc[(df_old["served"] == 1) & (df_old["start_svc"] >= 120.0), "start_svc"].to_numpy()
    assert busy_at(df_old, after_old).max() > 2


def test_nhpp_hourly_counts():
    """T1-b: rates=[0.5, 3.0], 2.000 ngay: so khach moi gio nam trong CI95 cua lambda_h * 60."""
    rates = [0.5, 3.0]
    m = Model(rates, exp_service(0.01), theta=0.0, p_vip=0.0, hour_len=60.0)
    n_days = 2000
    counts = np.zeros((n_days, 2))
    for d in range(n_days):
        df = cs.simulate(m, [5, 5], seed=500 + d)
        counts[d] = np.bincount(df["hour"].to_numpy(dtype=int), minlength=2)[:2]
    for h, lam in enumerate(rates):
        mean = counts[:, h].mean()
        half = st.t.ppf(0.975, n_days - 1) * counts[:, h].std(ddof=1) / np.sqrt(n_days)
        assert abs(mean - lam * 60.0) <= half, f"gio {h}: {mean:.2f} vs {lam * 60.0}"


def test_blocker_respects_schedule():
    """T1-c: Trong moi gio h (bo 20 phut chuyen tiep dau gio) so quay ban <= schedule[h]."""
    sched = [3, 5, 2, 4]
    m = Model([4.0] * 4, exp_service(1.0), theta=0.0, p_vip=0.0, hour_len=60.0)
    df = cs.simulate(m, sched, seed=21)
    starts = df.loc[df["served"] == 1, "start_svc"].to_numpy()
    for h, c in enumerate(sched):
        t_h = starts[(starts >= h * 60.0 + 20.0) & (starts < (h + 1) * 60.0)]
        assert len(t_h) > 0
        assert busy_at(df, t_h).max() <= c
        assert busy_at(df, t_h).max() == c  # tai qua nen dung du c quay


def test_util_hourly_sums():
    """T1-g: Tong util_h * c_h * 60 + thoi gian ban sau dong cua = tong thoi gian phuc vu."""
    sched = [4, 5, 6, 5]
    m = Model([1.2, 1.6, 1.9, 1.5], exp_service(3.0), theta=0.1, p_vip=0.3, hour_len=60.0)
    df = cs.simulate(m, sched, seed=31)
    r = cs.rep_stats(df, sched, 60.0)
    busy_hours = sum(h["util"] * c * 60.0 for h, c in zip(r["hourly"], sched))
    total_svc = df.loc[df["served"] == 1, "svc"].sum()
    assert busy_hours + r["busy_after_close"] == pytest.approx(total_svc, abs=1e-6)
    assert all(0.0 <= h["util"] <= 1.0 + 1e-9 for h in r["hourly"])
