"""
tests/test_v51_fixes.py: Kiem thu cac ban sua V5.1 (docs/KE_HOACH_V5_1.md):
1. F10: optimize_schedule bao "feasible"; lich khong dat khi qua tai va c_cap nho
2. F10: sipp_schedule canh bao khi roi vao nhanh du phong
3. F6: SL gop cua _post_class_sl trung rep_stats; khach thuong <= gop khi tai cao (VIP uu tien)
"""

import numpy as np
import pytest

from common import Model, exp_service
import b_theory as th
import c_sim as cs
import d_experiments as dx


def test_unfinished_customers_flagged():
    """F11: theta = 0, ~1.800 khach trong 60 phut, 3 quay E[S] 3 phut (~1.060 khach den luc cat) -> con khach."""
    m = Model(rates=[30.0], service=exp_service(3.0), theta=0.0, p_vip=0.0, hour_len=60.0)
    with pytest.warns(UserWarning, match="chua xu ly xong"):
        df = cs.simulate(m, [3], seed=7)
    assert df.attrs["n_unfinished"] > 0


def test_no_flag_when_all_finished():
    import warnings
    m = Model(rates=[1.0, 1.0], service=exp_service(3.0), theta=0.1, p_vip=0.3)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        df = cs.simulate(m, [5, 5], seed=7)
    assert "n_unfinished" not in df.attrs


def test_run_cache_identical_and_isolated(monkeypatch):
    """O1: bat / tat bo nho dem cho ket qua bang nhau; lan trung cache tra ban sao doc lap."""
    m, sched = _loaded(), [5, 6, 5]
    monkeypatch.setattr(cs, "CACHE_ON", False)
    ref = cs.run_reps(m, sched, n_reps=6, seed_base=9, keep_reps=True)
    monkeypatch.setattr(cs, "CACHE_ON", True)
    a = cs.run_reps(m, sched, n_reps=6, seed_base=9, keep_reps=True)
    a["hourly"][0]["sl_mean"] = -1.0
    a["rep_sl_day"][:] = -1.0
    b = cs.run_reps(_loaded(), sched, n_reps=6, seed_base=9, keep_reps=True)  # model moi, cung noi dung
    assert cs.CACHE_STATS == {"hit": 1, "miss": 1}
    for k, v in ref.items():
        if isinstance(v, np.ndarray):
            np.testing.assert_array_equal(v, b[k])
        else:
            assert v == b[k], k
    c = cs.run_reps(m, sched, n_reps=6, seed_base=10, keep_reps=True)  # seed khac -> chay lai
    assert cs.CACHE_STATS["miss"] == 2 and c["sl_mean"] != -1.0


def test_simulated_p_value():
    """S16: quan sat o trung vi -> p ~ 1; vuot moi mo phong -> p = 2/(K+1); nhat quan voi PI95."""
    import e_robustness as er
    sims = np.linspace(0.80, 1.00, 1000)
    assert er.simulated_p_value(sims, float(np.median(sims))) > 0.99
    assert er.simulated_p_value(sims, 1.5) == pytest.approx(2 / 1001)
    lo, hi = np.percentile(sims, [2.5, 97.5])
    for obs in np.linspace(lo + 1e-6, hi - 1e-6, 25):  # trong PI95 -> khong co y nghia o muc 5%
        assert er.simulated_p_value(sims, obs) >= 0.05


def _loaded():
    return Model(rates=[1.6, 1.9, 1.7], service=exp_service(3.0), theta=0.1, p_vip=0.35, mean_svc=3.0)


@pytest.mark.parametrize("seed", range(3))
def test_class_sl_gop_matches_rep_stats(seed):
    sched = [5, 6, 5]
    df = cs.simulate(_loaded(), sched, seed=seed)
    mat = dx._post_class_sl(df, sched)
    assert list(mat[0]) == [h["sl"] for h in cs.rep_stats(df, sched)["hourly"]]


@pytest.mark.parametrize("seed", range(3))
def test_rep_stats_sl_reg_matches_class_table(seed):
    """M9: sl_reg cua rep_stats trung SL khach thuong cua bang F6."""
    sched = [5, 6, 5]
    df = cs.simulate(_loaded(), sched, seed=seed)
    assert [h["sl_reg"] for h in cs.rep_stats(df, sched)["hourly"]] == list(dx._post_class_sl(df, sched)[1])


def test_feasible_scope_regular():
    """M9: scope="regular" xet sl_reg_ci95_low; mac dinh xet SL moi khach."""
    res = {"hourly": [{"hour": 0, "sl_ci95_low": 0.93, "sl_reg_ci95_low": 0.89},
                      {"hour": 1, "sl_ci95_low": 0.95, "sl_reg_ci95_low": 0.92}], "p_ab_mean": 0.0, "p_ab_ci_half": 0.0}
    assert cs.is_schedule_feasible(res) == (True, [])
    assert cs.is_schedule_feasible(res, scope="regular") == (False, [0])


def test_class_sl_regular_not_above_all():
    sched = [5, 6, 5]
    mats = np.stack([dx._post_class_sl(cs.simulate(_loaded(), sched, seed=100 + s), sched) for s in range(20)])
    gop, thuong = np.nanmean(mats[:, 0], axis=0), np.nanmean(mats[:, 1], axis=0)
    assert np.all(thuong <= gop + 1e-12)
    assert np.any(thuong < gop - 0.01)  # tai cao: uu tien VIP lam khach thuong cho lau hon ro


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
